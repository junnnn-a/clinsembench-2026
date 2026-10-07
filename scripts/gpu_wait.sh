# usage: source scripts/gpu_wait.sh; gpu_wait <min_free_MiB> [timeout_sec]
# Blocks until the GPU has at least <min_free_MiB> free. Our own queues are serialised with a file lock that is
# kept for HOLD seconds after the wait returns, so that the job just launched has allocated its memory before the
# next waiter measures free memory (several waiters used to pass at once and then OOM each other).
# Jobs of other projects on the same GPU do not take the lock; callers still need retries.
GPU_LOCK=/home/irteam/junah-data-1/ARR_10/2_ClimSemBench/logs/.gpu.lock
gpu_wait() {
  local need=$1 timeout=${2:-7200} hold=${GPU_HOLD:-150} waited=0
  exec 9>"$GPU_LOCK"
  flock 9
  while true; do
    local free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)
    if [ "$free" -ge "$need" ]; then
      echo "[gpu_wait] free=${free}MiB >= ${need}MiB"
      ( sleep "$hold" ) 9>&9 &        # background holder keeps the lock for $hold s
      exec 9>&-
      return 0
    fi
    if [ "$waited" -ge "$timeout" ]; then echo "[gpu_wait] timeout (free=${free}MiB < ${need}MiB)"; exec 9>&-; return 1; fi
    sleep 20; waited=$((waited+20))
  done
}
