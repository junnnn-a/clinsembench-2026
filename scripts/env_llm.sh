# source this before running anything with envs/llm (vLLM). See docs/4 §1 for why each line exists.
ROOT=/home/irteam/junah-data-1/ARR_10/2_ClimSemBench
export HF_HOME=/home/irteam/hf_cache
export HF_HUB_OFFLINE=1
export LD_LIBRARY_PATH=$ROOT/envs/llm/lib:${LD_LIBRARY_PATH:-}
export PATH=$ROOT/envs/llm/bin:$PATH
export CC=$ROOT/envs/llm/bin/gcc
export CXX=$ROOT/envs/llm/bin/g++
export VLLM_USE_FLASHINFER_SAMPLER=0      # no nvcc on this machine -> FlashInfer JIT sampler cannot build
export TOKENIZERS_PARALLELISM=false
PY=$ROOT/envs/llm/bin/python

# fixed KV-cache size (GiB) for vLLM: skips free-memory profiling, which breaks when other jobs share the GPU during start-up (10/7)
export KV_GB=${KV_GB:-16}
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-8} MKL_NUM_THREADS=${MKL_NUM_THREADS:-8}
