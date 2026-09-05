"""Check the encoded lesson, exact edit inputs and causal flow constraints."""
import hashlib
import math
import unittest
from unittest.mock import patch

import av
import numpy as np

from episode_infographics import EpisodeInfographics, ROOT, read, digest

OUT = ROOT / 'samples/content-catalog/interlock-agent-operation'


class EpisodeCutaways(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.editor = EpisodeInfographics()

    def test_film_and_all_render_inputs_match_receipts(self):
        receipt = read(OUT / 'infographic-edit.receipt.json')
        film = read(OUT / 'film.receipt.json')
        self.assertEqual(film['infographicEdit']['sha256'], digest(OUT / 'infographic-edit.receipt.json'))
        self.assertEqual(receipt['filmDigest'], digest(OUT / 'episode-01.mp4'))
        self.assertEqual(film['filmDigest'], receipt['filmDigest'])
        for path, expected in receipt['inputs'].items():
            self.assertEqual(digest(ROOT / path), expected, path)
        self.assertEqual(receipt['chapters'], self.editor.edit['chapters'])
        self.assertEqual(receipt['plans'], {key: plate.plan for key, plate in self.editor.plates.items()})
        self.assertFalse(film['liveEnforcementClaimed'])

    def test_narration_retiming_is_continuous_and_never_reverses(self):
        for id, spec in self.editor.edit['chapters'].items():
            duration = self.editor.chapters[id]['duration']
            for key, knots in spec['flowCues'].items():
                times = np.linspace(0, duration, 1000)
                values = [self.editor.flow_time(spec, key, t) for t in times]
                self.assertTrue(np.all(np.diff(values) >= 0))
                self.assertEqual(values[0], 0)
                self.assertAlmostEqual(values[-1], self.editor.plates[key].plan['duration'])
                for t, anchor in knots:
                    self.assertAlmostEqual(self.editor.flow_time(spec, key, t), self.editor.plates[key].anchor(anchor))

    def test_early_join_arrival_parks_at_exact_hub(self):
        plate = self.editor.plates['certification']
        join = plate.plan['nodes']['join']
        before = sum(join['arrivals']) / 2
        self.assertLess(min(join['arrivals']), before)
        self.assertLess(before, max(join['arrivals']))
        outbound = next(f for f in plate.plan['flights'] if f['source'] == 'join')
        self.assertGreaterEqual(outbound['start'], max(join['arrivals']))
        hub = np.array(plate.projection['layout']['junctionGlyphs']['join']['hub'])
        with patch.object(plate, 'ball') as draw_ball:
            plate.frame(before)
            points = [call.args[1] for call in draw_ball.call_args_list]
        self.assertTrue(any(np.linalg.norm(point - hub) < 1e-8 for point in points))
        for flight in plate.plan['flights']:
            if flight['target'] == 'join':
                np.testing.assert_allclose(plate.arcs[flight['id']].point(plate.arcs[flight['id']].length), hub)
            if flight['source'] == 'join':
                np.testing.assert_allclose(plate.arcs[flight['id']].point(0), hub)

    def test_current_branch_and_target_gap_do_not_gain_execution(self):
        current = self.editor.plates['current']
        self.assertEqual(current.plan['terminals'], ['allow'])
        self.assertNotIn('operator', current.plan['nodes'])
        target = self.editor.plates['certification']
        self.assertNotIn('proof', target.plan['nodes'])
        self.assertEqual(next(n for n in target.projection['nodes'] if n['id']=='proof')['basis'], 'GAP')
        for plate in (current, target):
            types = {e['id']: e['type'] for e in plate.projection['edges']}
            self.assertTrue(all(types[f['id']] in ('transition', 'product-transfer') for f in plate.plan['flights']))
        scene = self.editor.edit['chapters']['evidence']['scenes'][0]
        self.assertIn('TARGET', scene['basisLabel'])
        self.assertIn('LIVE PROOF REQUIRED', scene['basisLabel'])

    def test_encoded_movie_contains_the_declared_1080p_cutaways(self):
        with av.open(str(OUT / 'episode-01.mp4')) as movie:
            stream = movie.streams.video[0]
            self.assertEqual((stream.width, stream.height), (1920, 1080))
            self.assertEqual(float(stream.average_rate), 24)
            self.assertEqual(stream.frames, math.ceil(self.editor.timeline['durationSeconds']*24))
            self.assertEqual(len(movie.streams.audio), 1)
            for id, local in [('open-event', 4), ('open-event', 13), ('evidence', 5.9), ('evidence', 19)]:
                chapter = self.editor.chapters[id]
                frame_index = round((chapter['start']+local)*24)
                target_time = frame_index / 24
                movie.seek(int(target_time / stream.time_base), stream=stream, backward=True)
                actual = next(frame for frame in movie.decode(stream) if float(frame.pts*stream.time_base) >= target_time-1e-5)
                expected = np.asarray(self.editor.frame(chapter, target_time-chapter['start']), dtype=float)
                pixels = actual.to_ndarray(format='rgb24').astype(float)
                rmse = np.sqrt(np.mean((pixels-expected)**2))
                self.assertLess(rmse, 5, f'{id}@{local}: source cutaway missing or stale (RMSE {rmse})')

    def test_encoded_narration_matches_the_previous_film(self):
        baseline = read(ROOT / 'evaluations/episode-01-infographic-review.json')['audio']
        sha = hashlib.sha256(); samples = 0
        with av.open(str(OUT / 'episode-01.mp4')) as movie:
            for frame in movie.decode(audio=0):
                sha.update(frame.to_ndarray().tobytes()); samples += frame.samples
        self.assertEqual(sha.hexdigest(), baseline['decodedAudioSha256'])
        self.assertEqual(samples, baseline['decodedAudioSamples'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
