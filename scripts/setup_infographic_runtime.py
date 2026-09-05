"""Verify and install one portable official Graphviz distribution in this lab."""
import urllib.request
import zipfile
from infographic_contract import ROOT,digest,write

URL='https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/14.1.2/windows_10_cmake_Release_Graphviz-14.1.2-win64.zip'
SHA='dac16e24dda53d3b94a4ffa9176bf10a3de7f419060a67a3b4882d06234d61ff'
DOT_SHA='cd49d13e48d591f62ea4ab1e64b060abdb804c5ec6b34ffa878711ba954d1652'

def main():
    tools=ROOT/'.tools';tools.mkdir(exist_ok=True);archive=tools/'graphviz-14.1.2.zip';destination=tools/'graphviz-14.1.2'
    if not archive.exists():urllib.request.urlretrieve(URL,archive)
    if digest(archive)!=SHA:raise ValueError('GRAPHVIZ_ARCHIVE_DIGEST_MISMATCH')
    dot=destination/'Graphviz-14.1.2-win64/bin/dot.exe'
    if not dot.exists():
        with zipfile.ZipFile(archive) as package:
            for member in package.infolist():
                if not (destination/member.filename).resolve().is_relative_to(destination.resolve()):raise ValueError('ARCHIVE_PATH_ESCAPE')
            package.extractall(destination)
    if digest(dot)!=DOT_SHA:raise ValueError('GRAPHVIZ_EXECUTABLE_DIGEST_MISMATCH')
    write('data/infographic-runtime.json',{'graphvizVersion':'14.1.2','officialArchive':URL,'archiveSha256':SHA,'executableSha256':DOT_SHA,'executable':dot.relative_to(ROOT).as_posix(),'installationScope':'Content lab only; no system PATH change.'})
    print('Verified portable Graphviz 14.1.2.')

if __name__=='__main__':main()
