import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import plotly.express as px
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import correlation, cosine
from evaluate_recording.feature_extractor import extract_features

sessions_list = [1, 2, 3]

window_ms = 0.100

merged_dict = {}

esc50_df = pd.read_csv('/home/danial/Documents/Projects/Personal/AuditoryModeling/data/esc_50/esc50.csv')

for session in sessions_list:
    with open(f'/home/danial/Documents/Projects/Personal/AuditoryModeling/data/recording_data/session{session}.pkl',
              'rb') as handle:
        recording_dict = pickle.load(handle)
    features = extract_features(recording_dict, window_size=window_ms, session=session)
    merged_dict = {**merged_dict, **features}

# print(len(merged_dict))
#
# print(merged_dict.keys())

# color_map = {}
# label_set = set(labels_class_names)
# for index, l in enumerate(label_set):
#     color_map[l] = hex_colors[index]


labels_set = []
features_set = []
file_names = []
for idx, (stimulus, attributes) in enumerate(merged_dict.items()):

    if idx == 43 or idx == 35:
        continue
    # print(stimulus, attributes['features'].shape)
    if ".wav" in stimulus:
        category = esc50_df.loc[esc50_df['filename'] == stimulus, 'category'].values[0]
    else:
        category = "tone"  # stimulus.split('-')[1]

    labels_set.append(category)
    features = attributes['features']
    mask = attributes['mask']

    features = np.mean(features, axis=0)
    features = features[mask, :]
    features = np.mean(features, axis=0)
    features_set.append(features)
    file_names.append(stimulus)
    # print(features.shape)

features_set = np.asarray(features_set)
print(features_set.shape)
# features_set = np.delete(features_set, 35, 0)

# features_set = np.delete(features_set, 42, 0)

labels_set = np.asarray(labels_set)
print(file_names)

# Define the list of labels to remove
labels_to_remove = ['tone']

# Convert labels_set to a numpy array if it's not already
labels_set = np.asarray(labels_set)
file_names = np.asarray(file_names)

# Find indices of labels that are not in the list of labels to remove
indices_to_keep = np.where(~np.isin(labels_set, labels_to_remove))[0]

# Filter both features_set and labels_set based on the indices to keep
features_set = features_set[indices_to_keep]
labels_set = labels_set[indices_to_keep]
file_names = file_names[indices_to_keep]

print(np.unique(labels_set))
print(len(np.unique(labels_set)))

# KNN:
X_train, X_test, y_train, y_test = train_test_split(features_set, labels_set,
                                                    test_size=0.2)

# Scale the features using StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)



sorted_indices = np.lexsort((file_names, labels_set))

# Sort features based on the sorted indices
features_set = features_set[sorted_indices]

# Optionally, also sort labels and file_names if needed
labels_set = labels_set[sorted_indices]
file_names = file_names[sorted_indices]

correlation_matrix = 1 - np.corrcoef(features_set)

plt.imshow(correlation_matrix, interpolation='nearest')
plt.savefig('corr_matrix.png')

distances = []
for i in range(12):
    with open(f'/home/danial/Documents/Projects/Personal/AuditoryModeling/data_analysis/results2/rdm_beats_{i}.pkl', 'rb') as handle:
        b = pickle.load(handle)
        distance = 1 - correlation(correlation_matrix.reshape(-1), b.reshape(-1))
        distances.append(distance)
print(distances)


#
# plt.figure(figsize=(8, 6))
#
# pca = PCA(n_components=2)  # You can adjust the number of components as needed
# X_pca = pca.fit_transform(features_set)
#
# for label in np.unique(labels_set):
#     plt.scatter(X_pca[labels_set == label, 0], X_pca[labels_set == label, 1], label=label)
#
# plt.title('PCA of Your Data')
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.legend()
# plt.show()
tsne = TSNE(n_components=2, random_state=42)
components = tsne.fit_transform(features_set)

df = pd.DataFrame(
    data={'PC1': components[:, 0], 'PC2': components[:, 1], 'Label': labels_set, 'file_name': file_names})

df.to_csv('results/env_tsne_a1.csv')

# Create scatter plot with hover text
fig = px.scatter(df, x='PC1', y='PC2', color='Label', hover_data=['Label', 'file_name'],
                 opacity=0.7)

# Show the plot
fig.show()

# Save the plot as an image
fig.write_image(f"results/env_tsne_a1.png")


