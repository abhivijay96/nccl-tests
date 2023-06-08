/*************************************************************************
 * Copyright (c) 2016-2022, NVIDIA CORPORATION. All rights reserved.
 *
 * See LICENSE.txt for license information
 ************************************************************************/

#include "cuda_runtime.h"
#include "common.h"

void latencyGetCollByteCount(size_t *sendcount, size_t *recvcount, size_t *paramcount, size_t *sendInplaceOffset, size_t *recvInplaceOffset, size_t count, int nranks) {
  *sendcount = count;
  *recvcount = count;
  *sendInplaceOffset = 0;
  *recvInplaceOffset = 0;
  *paramcount = *sendcount;
}

testResult_t latencyInitData(struct threadArgs* args, ncclDataType_t type, ncclRedOp_t op, int root, int rep, int in_place) {
  size_t sendcount = args->sendBytes / wordSize(type);
  size_t recvcount = args->expectedBytes / wordSize(type);
  int nranks = args->nProcs*args->nThreads*args->nGpus;

  for (int i=0; i<args->nGpus; i++) {
    CUDACHECK(cudaSetDevice(args->gpus[i]));
    int rank = ((args->proc*args->nThreads + args->thread)*args->nGpus + i);
    CUDACHECK(cudaMemset(args->recvbuffs[i], 0, args->expectedBytes));
    void* data = in_place ? args->recvbuffs[i] : args->sendbuffs[i];
    TESTCHECK(InitData(data, sendcount, rank*sendcount, type, ncclSum, rep, 1, 0));
    int peer = (rank-1+nranks)%nranks;
    TESTCHECK(InitData(args->expected[i], recvcount, peer*recvcount, type, ncclSum, rep, 1, 0));
    CUDACHECK(cudaDeviceSynchronize());
  }
  // We don't support in-place latency
  args->reportErrors = in_place ? 0 : 1;
  return testSuccess;
}

void latencyGetBw(size_t count, int typesize, double sec, double* algBw, double* busBw, int nranks) {
  double baseBw = (double)(count * typesize) / 1.0E9 / sec;

  *algBw = baseBw;
  double factor = 1;
  *busBw = baseBw * factor;
}

testResult_t latencyRunColl(void* sendbuff, void* recvbuff, size_t count, ncclDataType_t type, ncclRedOp_t op, int root, ncclComm_t*  comm_ptr, cudaStream_t stream) {
  ncclComm_t comm = *comm_ptr;
  int nRanks;
  NCCLCHECK(ncclCommCount(comm, &nRanks));
  int rank;
  NCCLCHECK(ncclCommUserRank(comm, &rank));
  
  if(nRanks != 2) {
    printf("Invalid usage of latency script, only two GPUs can be passed, L is sender, R is receiver.\n");
    return testInternalError;
  }

  int senderRank = 0;
  int receiverRank = 1;

  NCCLCHECK(ncclGroupStart());
  if(rank == senderRank) {
    NCCLCHECK(ncclSend(sendbuff, count, type, receiverRank, comm, stream));
  }
  if(rank == receiverRank) {
    NCCLCHECK(ncclRecv(recvbuff, count, type, senderRank, comm, stream));
  }
  NCCLCHECK(ncclGroupEnd());
  
  return testSuccess;
}

struct testColl latencyTest = {
  "latency",
  latencyGetCollByteCount,
  latencyInitData,
  latencyGetBw,
  latencyRunColl
};

void latencyGetBuffSize(size_t *sendcount, size_t *recvcount, size_t count, int nranks) {
  size_t paramcount, sendInplaceOffset, recvInplaceOffset;
  latencyGetCollByteCount(sendcount, recvcount, &paramcount, &sendInplaceOffset, &recvInplaceOffset, count, nranks);
}

testResult_t latencyRunTest(struct threadArgs* args, int root, ncclDataType_t type, const char* typeName, ncclRedOp_t op, const char* opName) {
  args->collTest = &latencyTest;
  ncclDataType_t *run_types;
  ncclRedOp_t *run_ops;
  const char **run_typenames, **run_opnames;
  int type_count, op_count;

  if ((int)type != -1) {
    type_count = 1;
    run_types = &type;
    run_typenames = &typeName;
  } else {
    type_count = test_typenum;
    run_types = test_types;
    run_typenames = test_typenames;
  }

  if ((int)op != -1) {
    op_count = 1;
    run_ops = &op;
    run_opnames = &opName;
  } else {
    op_count = test_opnum;
    run_ops = test_ops;
    run_opnames = test_opnames;
  }

  for (int i=0; i<type_count; i++) {
    for (int j=0; j<op_count; j++) {
      TESTCHECK(TimeTest(args, run_types[i], run_typenames[i], run_ops[j], run_opnames[j], -1));
    }
  }
  return testSuccess;
}

struct testEngine latencyEngine = {
  latencyGetBuffSize,
  latencyRunTest
};

#pragma weak ncclTestEngine=latencyEngine
