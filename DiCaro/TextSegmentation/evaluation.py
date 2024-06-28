from nltk.metrics.segmentation import pk, windowdiff, ghd
import random
# hyp = []
# with open('evaluation/hyp_DA_4_0166.txt', 'r') as f:
#     for line in f.readlines():
#         sentences = line.split('.')
#         hyp.extend([0] * (len(sentences) - 2))
#         hyp.append(1)
# print("hyp_DA_4_0166 = ", hyp)
# # print("len:", len(hyp))
# # for pos in range(len(hyp)):
# #     if hyp[pos] == 1:
# #         print(pos + 1)
#
#
# hyp = []
# with open('evaluation/hyp_DA_6_02.txt', 'r') as f:
#     for line in f.readlines():
#         sentences = line.split('.')
#         hyp.extend([0] * (len(sentences) - 2))
#         hyp.append(1)
# print("hyp_DA_6_02 = ", hyp)
# # print("len:", len(hyp))
# # for pos in range(len(hyp)):
# #     if hyp[pos] == 1:
# #         print(pos + 1)
#
#
# hyp = []
# with open('evaluation/hyp_DA_10_0.txt', 'r') as f:
#     for line in f.readlines():
#         sentences = line.split('.')
#         hyp.extend([0] * (len(sentences) - 2))
#         hyp.append(1)
# print("hyp_DA_10_0 = ", hyp)
# # print("len:", len(hyp))
# # for pos in range(len(hyp)):
# #     if hyp[pos] == 1:
# #         print(pos + 1)
#
# ref = []
# with open('evaluation/refDA.txt', 'r') as f:
#     for line in f.readlines():
#         sentences = line.split('.')
#         ref.extend([0] * (len(sentences) - 2))
#         ref.append(1)
# print("refDA = ", ref)
# # print("len:", len(ref))
# # for pos in range(len(ref)):
# #     if ref[pos] == 1:
# #         print(pos + 1)

# hyp_RS_4_005 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
# hyp_RS_3_005 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
# hyp_RS_6_0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
# ref_RS = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
hyp_DA_4_0166 =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
hyp_DA_6_02 =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
hyp_DA_10_0 =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
refDA =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

ref_segments = [-1]
for s in range(len(refDA)):
    if refDA[s] == 1:
        ref_segments.append(s)

print(ref_segments)

hyp_segments = [-1]
for s in range(len(hyp_DA_4_0166)):
    if hyp_DA_4_0166[s] == 1:
        hyp_segments.append(s)

print(hyp_segments)

segments_size = []
for i in range(len(ref_segments) - 1):
    segments_size.append(ref_segments[i + 1] - ref_segments[i] - 1)
for i in range(len(hyp_segments) - 1):
    segments_size.append(hyp_segments[i + 1] - hyp_segments[i] - 1)



sum = 0
for size in segments_size:
    sum += size
k_DA_4_0166 = int(sum / (len(segments_size) * 2))
print("k_DA_4_0166 = ", k_DA_4_0166)


hyp_segments = [-1]
for s in range(len(hyp_DA_6_02)):
    if hyp_DA_6_02[s] == 1:
        hyp_segments.append(s)

print(hyp_segments)

segments_size = []
for i in range(len(ref_segments) - 1):
    segments_size.append(ref_segments[i + 1] - ref_segments[i] - 1)
for i in range(len(hyp_segments) - 1):
    segments_size.append(hyp_segments[i + 1] - hyp_segments[i] - 1)

print(segments_size)

sum = 0
for size in segments_size:
    sum += size
k_DA_6_02 = int(sum / (len(segments_size) * 2))
print("k_DA_6_02 = ", k_DA_6_02)


hyp_segments = [-1]
for s in range(len(hyp_DA_10_0)):
    if hyp_DA_10_0[s] == 1:
        hyp_segments.append(s)

print(hyp_segments)

segments_size = []
for i in range(len(ref_segments) - 1):
    segments_size.append(ref_segments[i + 1] - ref_segments[i] - 1)
for i in range(len(hyp_segments) - 1):
    segments_size.append(hyp_segments[i + 1] - hyp_segments[i] - 1)

print(segments_size)

sum = 0
for size in segments_size:
    sum += size
k_DA_10_0 = int(sum / (len(segments_size) * 2))
print("k_DA_10_0 = ", k_DA_10_0)

ref_RS_str = ''.join(str(x) for x in refDA)
hyp_DA_4_0166_str = ''.join(str(x) for x in hyp_DA_4_0166)
hyp_DA_6_02_str = ''.join(str(x) for x in hyp_DA_6_02)
hyp_DA_10_0_str = ''.join(str(x) for x in hyp_DA_10_0)

print("pk")
print('k_DA_4_0166', '%.2f' % pk(ref_RS_str, hyp_DA_4_0166_str, k_DA_4_0166))
print('k_DA_6_02', '%.2f' % pk(ref_RS_str, hyp_DA_6_02_str, k_DA_6_02))
print('k_DA_10_0', '%.2f' % pk(ref_RS_str, hyp_DA_10_0_str, k_DA_10_0))
print("windowdiff")
print('k_DA_4_0166', '%.2f' % windowdiff(ref_RS_str, hyp_DA_4_0166_str, k_DA_4_0166))
print('k_DA_6_02', '%.2f' % windowdiff(ref_RS_str, hyp_DA_6_02_str, k_DA_6_02))
print('k_DA_10_0', '%.2f' % windowdiff(ref_RS_str, hyp_DA_10_0_str, k_DA_10_0))
print("ghd")
print('%.2f' % ghd(ref_RS_str, hyp_DA_4_0166_str, k_DA_4_0166, k_DA_4_0166, 2))
print('%.2f' % ghd(ref_RS_str, hyp_DA_6_02_str, k_DA_6_02, k_DA_6_02, 2))
print('%.2f' % ghd(ref_RS_str, hyp_DA_10_0_str, k_DA_10_0, k_DA_10_0, 2))
#
#
# segments_size = []
# for i in range(len(ref_segments) - 1):
#     segments_size.append(ref_segments[i + 1] - ref_segments[i] - 1)
#
# print(ref_segments)
# print(segments_size)
# sum = 0
# for size in segments_size:
#     sum += size
# print(sum / len(segments_size))