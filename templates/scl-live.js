'use strict';
// One compilation at a time. Edits replace queued work and invalidate older results.
class SCLLiveCompiler {
  constructor({execute, start=()=>{}, success=()=>{}, error=()=>{}, timers=globalThis}) {
    Object.assign(this,{execute,start,success,error,timers});
    this.revision=0;this.pending=null;this.running=false;this.timer=null;
  }
  invalidate() {
    ++this.revision;this.pending=null;
    this.timers.clearTimeout(this.timer);this.timer=null;
  }
  schedule(value,delay=0) {
    this.invalidate();
    const job={value,revision:this.revision,ready:delay===0};this.pending=job;
    if(delay) this.timer=this.timers.setTimeout(()=>{this.timer=null;job.ready=true;this.drain();},delay);
    this.drain();
  }
  async drain() {
    if(this.running||!this.pending?.ready)return;
    const job=this.pending;this.pending=null;this.running=true;
    try {
      this.start(job.value);
      const result=await this.execute(job.value);
      if(job.revision===this.revision)this.success(result,job.value);
    } catch(error) {
      if(job.revision===this.revision)this.error(error,job.value);
    } finally {this.running=false;this.drain();}
  }
}
if(typeof module!=='undefined')module.exports=SCLLiveCompiler;
