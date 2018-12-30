

###########################################################################################################################



###########################################################################################################################


###########################################################################################################################


###########################################################################################################################



###########################################################################################################################

 X_train = np.zeros((num_train_samples, img_width, img_height, num_channels))
input_shape = (img_width, img_height, 3) 
or 
input_shape = (img_height, img_width, 3)
###########################################################################################################################
for d in ['/device:GPU:0', '/device:GPU:1']:
    with tf.device(d):
        history = model.fit_generator(
          train_generator,
          steps_per_epoch = nb_train_samples // batch_size,
          epochs = epochs,
          validation_data = validation_generator,
          validation_steps = nb_validation_samples // batch_size)
###########################################################################################################################
# Generate training data using gpu:0
with tf.device('/GPU:0'):
        # Set up generator for training data
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            featurewise_center=True,
            featurewise_std_normalization=True)

        # Generate training data
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(img_height, img_width),
            batch_size=batch_size,
            seed = random_seed,
            shuffle = True,
            class_mode='categorical')

with tf.device('/GPU:1'):
         # Generate validation data using gpu:1
            validation_generator = train_datagen.flow_from_directory(
                validation_dir,
                target_size=(img_height, img_width),
                batch_size=batch_size,
                seed = random_seed,
                shuffle = True,
                class_mode='categorical')

            test_datagen = ImageDataGenerator(rescale=1. / 255)

            test_generator = test_datagen.flow_from_directory(
                test_dir,
                target_size=(img_height, img_width),
                batch_size=batch_size,
                seed = random_seed,
                shuffle = False,
                class_mode='categorical')

###########################################################################################################################

model = Sequential()

model.add(
    Conv2D(
        filters=64,
        kernel_size=(3, 3),
        activation="relu",
        input_shape=(224, 224, 3)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(filters=128, kernel_size=(3, 3), activation="relu"))
model.add(Conv2D(filters=128, kernel_size=(3, 3), activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(filters=256, kernel_size=(3, 3), activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3, 3), activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3, 3), activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(filters=512, kernel_size=(3, 3), activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3, 3), activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3, 3), activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(filters=512, kernel_size=(3, 3), activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3, 3), activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3, 3), activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(units=1024, activation="relu"))
model.add(Dense(units=1024, activation="relu"))
model.add(Dense(units=12, activation="softmax"))


###########################################################################################################################

from keras.models import load_model
model = load_model("models/5.VGG19-Adam-Dropout-Model.h5")
model.load_weights("models/VGG19-Adam-Dropout-Weights.h5")

###########################################################################################################################
import _pickle as cPickle
import pickle
###########################################################################################################################
from tqdm import tqdm


X_train, y_train = [], []
for _ in tqdm(range(nb_train_samples)):
    x, y = train_generator.next()
    X_train.append(x[0])
    y_train.append(y[0])
X_train = np.asarray(X_train)
y_train = np.asarray(y_train)
y_train = np.argmax(y_train, axis=1)

X_validation, y_validation = [], []
for _ in tqdm(range(nb_validation_samples)):
    x_val, y_val = validation_generator.next()
    X_validation.append(x_val[0])
    y_validation.append(y_val[0])
X_validation = np.asarray(X_validation)
y_validation = np.asarray(y_validation)
y_validation = np.argmax(y_validation, axis=1)
# np.save('data/npy/X_validation.npy', X_validation)
# np.save('data/npy/y_validation.npy', y_validation)

X_test, y_test = [], []
for _ in tqdm(range(nb_test_samples)):
    x_t, y_t = test_generator.next()
    X_test.append(x_t[0])
    y_test.append(y_t[0])
X_test = np.asarray(X_test)
y_test = np.asarray(y_test)
y_test = np.argmax(y_test, axis=1)
# np.save('data/npy/X_test.npy', X_test)
# np.save('data/npy/y_test.npy', y_test)

nb_train_samples = 386
nb_validation_samples = 199
nb_test_samples = 155
###########################################################################################################################

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import *
from keras.layers import *
from keras.regularizers import *
from keras.optimizers import *

from keras import applications

###########################################################################################################################
import keras
import tensorflow as tf
from keras import backend as K

print("Keras Version:", keras.__version__)
print("Tensorflow Version:", tf.__version__)
print("image dim ordering:", K.image_dim_ordering())
###########################################################################################################################

    
from keras.applications import ResNet50
from keras.layers import Flatten, Dense, Dropout, BatchNormalization
from keras.regularizers import l2

model_dense_conv = ResNet50(weights='imagenet', include_top=False)  
    #Create your own input format
keras_input = Input(shape= input_shape, name = 'image_input')
    
    #Use the generated model 
output_dense_conv = model_dense_conv(keras_input)
    
    #Add the fully-connected layers 
x = Flatten(name='flatten')(output_dense_conv)
x = Dense(1024, activation= 'relu', kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001), name='fc1')(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)
x = Dense(1024, activation= 'relu', kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001), name='fc2')(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)
x = Dense(output_classes, activation='softmax', kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001), name='predictions')(x)
    
    #Create your own model 
model = Model(inputs=keras_input, outputs=x)

###########################################################################################################################
# extract the features from the second to the last fc layer
intermediate_lyr_model = Model(inputs=model.input,outputs=model.get_layer('fc2').output)
###########################################################################################################################
# Clean up Keras session by clearing memory. 
if K.backend()== 'tensorflow':
K.clear_session()
###########################################################################################################################
x = model.layers[-5].output
x = Flatten()(x)
###########################################################################################################################

from keras.applications import DenseNet201

base_model = DenseNet201(weights='imagenet', include_top=False, input_tensor=Input(shape=input_shape))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001))(x)
x = BatchNormalization()(x)
x = Activation("relu")(x)
x = Dropout(0.5)(x)
x = Dense(1024, kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001))(x)
x = BatchNormalization()(x)
x = Activation("relu")(x)
x = Dropout(0.5)(x)
prediction = Dense(output_classes, activation=tf.nn.softmax)(x)

model = Model(inputs=base_model.input,outputs=prediction)
###########################################################################################################################


total=sum(sum(cm))

accuracy = (cm[0,0]+cm[1,1]) / total
print ('Accuracy : ', accuracy)

sensitivity = cm[0,0]/(cm[0,0]+cm[1,0])
print('Sensitivity : ', sensitivity )

Specificity = cm[1,1]/(cm[1,1]+cm[0,1])
print('Specificity : ', Specificity )

###########################################################################################################################
# softmax dense error
prediction = Dense(output_classes, activation=tf.nn.softmax)(x)
or 
model.add(Activation(tf.nn.softmax))

###########################################################################################################################
sgd_opt = SGD(lr=1e-3, decay=1e-6, momentum=0.9, nesterov=True)

adam_opt = Adam(lr=1e-5, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=1e-5)
sgd_opt = SGD(lr=1e-06, momentum=0.0, decay=0.0, nesterov=False)

rmsp_opt = RMSprop(lr=1e-4, decay=0.9)
###########################################################################################################################
from keras import backend as K
K.image_data_format()

K.set_image_data_format('channels_first')
K.image_data_format()
###########################################################################################################################
from tensorflow.python.client import device_lib
device_lib.list_local_devices()
###########################################################################################################################
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')


if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)
###########################################################################################################################
def lr_schedule(epoch):
    if epoch < 15:
        return .01
    elif epoch < 28:
        return .002
    else:
        return .0004

jobs_base_dir = 'jobs'
job_name = 'vgg19_job'
model_name = 'vgg19'
job_path = "{}/{}".format(jobs_base_dir, job_name)
tensorboard_dir = "{}/{}".format(job_path, "tensorboard")
  
weights_path = "{}/{}".format(job_path, "weights.{epoch:02d}-{val_loss:.2f}.hdf5")
checkpointer = ModelCheckpoint(filepath=weights_path, verbose=1, save_best_only=True)
csv_logger = CSVLogger("{}/{}.log".format(job_path, model_name))
early_stopping = EarlyStopping(monitor='val_loss', verbose=1, patience=25)
tensorboard = TensorBoard(log_dir="{}".format(tensorboard_dir), histogram_freq=0, batch_size=32, write_graph=True,
                          write_grads=False,
                          write_images=True, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)
lr_scheduler = LearningRateScheduler(lr_schedule)


history = model.fit_generator(train_generator,
#     steps_per_epoch=nb_train_samples // batch_size,
    steps_per_epoch= 2048,
    epochs = 50,
    validation_data = validation_generator,
#     validation_steps=nb_validation_samples // batch_size,
    validation_steps = 1048,
    callbacks=[lr_scheduler, csv_logger, checkpointer, tensorboard, early_stopping])
###########################################################################################################################

#Reading in the dataset

df = pd.read_csv('fraud_prediction.csv')

#Dropping the target feature & the index

df = df.drop(['Unnamed: 0', 'isFraud'], axis = 1)

#Initializing K-means with 2 clusters

k_means = KMeans(n_clusters = 2)

#Fitting the model on the data

k_means.fit(df)

#Extracting labels 

target_labels = k_means.predict(df)

#Converting the labels to a series 

target_labels = pd.Series(target_labels)

#Merging the labels to the dataset

df = pd.merge(df, pd.DataFrame(target_labels), left_index=True, right_index=True)

#Renaming the target 

df['fraud'] = df[0]
df = df.drop([0], axis = 1)


from sklearn.manifold import TSNE

#Creating the features

features = df.drop('fraud', axis = 1).values

target = df['fraud'].values

#Initialize a TSNE object

tsne_object = TSNE()

#Fit and transform the features using the TSNE object

transformed = tsne_object.fit_transform(features)



#Creating a t-SNE visualization

x_axis = transformed[:,0]


y_axis = transformed[:,1]


plt.scatter(x_axis, y_axis, c = target)

plt.show()

###########################################################################################################################
# plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
N = epochs
plt.plot(np.arange(0, N), History.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), History.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), History.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), History.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="upper left")



###########################################################################################################################

from keras.applications import DenseNet201
model = DenseNet201(weights = "imagenet", include_top=False, input_shape = (img_rows, img_cols, 3))

from keras.layers import Flatten, Dense, Dropout, BatchNormalization
from keras.regularizers import l2
#Adding custom Layers 
x = model.output
x = Flatten()(x)
x = Dense(2048, activation="elu", kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001))(x)
x = BatchNormalization()(x)
# x = Dropout(0.5)(x)
x = Dense(1024, activation="elu", kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001))(x)
x = BatchNormalization()(x)
# x = Dropout(0.5)(x)
predictions = Dense(1, activation="sigmoid", kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001))(x)

from keras.models import Model
# creating the final model 
model_final = Model(input = model.input, output = predictions)
###########################################################################################################################
print("OS: ", sys.platform)
print("Python: ", sys.version)
print("Keras: ", K.__version__)
print("Numpy: ", np.__version__)
print("Tensorflow: ", tensorflow.__version__)
print(K.backend.backend())
print(K.backend.image_data_format())
print("GPU: ", get_gpu_name())
print(get_cuda_version())
print("CuDNN Version ", get_cudnn_version())


CPU_COUNT = multiprocessing.cpu_count()
GPU_COUNT = len(get_gpu_name())
print("CPUs: ", CPU_COUNT)
print("GPUs: ", GPU_COUNT)
##########################################################################################################################
# Create a generator for prediction
validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=(image_size, image_size),
        batch_size=1,
        class_mode='categorical',
        shuffle=False)

# Get the filenames from the generator
fnames = validation_generator.filenames

# Get the ground truth from generator
ground_truth = validation_generator.classes

# Get the label to class mapping from the generator
label2index = validation_generator.class_indices

# Getting the mapping from class index to class label
idx2label = dict((v,k) for k,v in label2index.items())

# Get the predictions from the model using the generator
predictions = model.predict_generator(validation_generator, steps=validation_generator.samples/validation_generator.batch_size,verbose=1)
predicted_classes = np.argmax(predictions,axis=1)
#print (predictions)

errors = np.where(predicted_classes != ground_truth)[0]
print("No of errors = {}/{}".format(len(errors),validation_generator.samples))

# Show the errors
for i in range(len(errors)):
    pred_class = np.argmax(predictions[errors[i]])
    pred_label = idx2label[pred_class]
    
    title = 'Original label:{}, Prediction :{}, confidence : {:.3f}, class ID : {}'.format(
        fnames[errors[i]].split('/')[0],
        pred_label,
        predictions[errors[i]][pred_class], pred_class)
    
    original = load_img('{}/{}'.format(validation_dir,fnames[errors[i]]))
    plt.figure(figsize=[7,7])
    plt.axis('off')
    plt.title(title)
    plt.imshow(original)
    plt.show()
#################################################################################################################
fnames = validation_generator2.filenames
 
ground_truth = validation_generator2.classes
 
label2index = validation_generator2.class_indices
 
# Getting the mapping from class index to class label
idx2label = dict((v,k) for k,v in label2index.items())
prob = model.predict_generator(validation_generator2)
predictions=np.argmax(prob,axis=1)

errors = np.where(predictions != ground_truth)[0]
print("No of errors = {}/{}".format(len(errors),nb_validation_samples))
####################################################################################################################
testing_generator = validation_datagen.flow_from_directory(
        test_dir,
        target_size=(height, width),
        batch_size=val_batchsize,
        class_mode='categorical',
        shuffle=False)
 
# Get the filenames from the generator
fnames = testing_generator.filenames
 
# Get the ground truth from generator
ground_truth = testing_generator.classes
 
# Get the label to class mapping from the generator
label2index = testing_generator.class_indices
 
# Getting the mapping from class index to class label
idx2label = dict((v,k) for k,v in label2index.items())
 
# Get the predictions from the model using the generator
predictions = model.predict_generator(testing_generator, 
                                      steps=testing_generator.samples/testing_generator.batch_size,
                                      verbose=1)
predicted_classes = np.argmax(predictions,axis=1)
 
errors = np.where(predicted_classes != ground_truth)[0]
print("No of errors = {}/{}".format(len(errors),testing_generator.samples))
print(str(len(errors)/testing_generator.samples) + "%")
####################################################################################################################
from tensorflow.python.client import device_lib
device_lib.list_local_devices()
####################################################################################################################
predictions = np.round(model_mura.predict_generator(test_generator, steps=3197//1))
predictions = predictions.flatten()
y_true = test_generator.classes

def print_all_metrics(y_true, y_pred):
    print("roc_auc_score: ", roc_auc_score(y_true, y_pred))
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    print("Sensitivity: ", get_sensitivity(tp, fn))
    print("Specificity: ", get_specificity(tn, fp))
    print("Cohen-Cappa-Score: ", cohen_kappa_score(y_true, y_pred))
    print("F1 Score: ", f1_score(y_true, y_pred))


def get_sensitivity(tp, fn):
    return tp / (tp + fn)


def get_specificity(tn, fp):
return tn / (tn + fp)


print_all_metrics(y_true,y_pred)

####################################################################################################################
####################################################################################################################
####################################################################################################################
model.fit(x_train, y_train, nb_epoch=5, batch_size=64, class_weight=myclass_weight)

	#Evaluate the scores of the model
	scores = model.evaluate(x_test, y_test, verbose=0)
	print("Accuracy: %.2f%%" % (scores[1]*100))
	probas = model.predict(x_test)
	pred_indices = np.argmax(probas, axis=1)
	classes = np.array(range(0,9))
	preds = classes[pred_indices]
	#model.save('../models/cnn_model4.h5')
	print('Log loss: {}'.format(log_loss(classes[np.argmax(y_test, axis=1)], probas)))
print('Accuracy: {}'.format(accuracy_score(classes[np.argmax(y_test, axis=1)], preds))) 


####################################################################################################################
model.fit(X_train, Y_train, validation_data=(X_valid,Y_valid),batch_size=32, \
              epochs=10, verbose=1)
score = model.evaluate(X_test, Y_test)
result = model.predict(X_test)
f1_score(Y_test, result, average='weighted')


####################################################################################################################


history = model.fit_generator(datagen.flow(train_X, train_y, batch_size=128),
epochs=100, validation_data=(valid_X, valid_y), workers=4)

pred_y = model.predict(test_X)
pred_y = np.argmax(pred_y, 1)
####################################################################################################################
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

model.fit_generator(datagen.flow(x_train, y_train,
                        batch_size=batch_size),
                        epochs=epochs,
                        workers=4)

y_pred = np.argmax(model.predict(x_test), axis=-1)
print(precision_score(y_test, y_pred, average='macro'))
print(recall_score(y_test, y_pred, average='macro'))
print(accuracy_score(y_test, y_pred))
print(f1_score(y_test, y_pred, average='macro'))



####################################################################################################################

model.compile(loss='categorical_crossentropy', optimizer='rmsprop',
metrics = ['categorical_accuracy', 'precision', 'recall', 'fmeasure'])

####################################################################################################################
from sklearn.metrics import classification_report, confusion_matrix

#Confution Matrix and Classification Report
Y_pred = model.predict_generator(test_generator)
y_pred = np.argmax(Y_pred, axis=1)
print('Confusion Matrix')
C = confusion_matrix(test_generator.classes, y_pred)
C_n = C.astype('float') / C.sum(axis=1)[:, np.newaxis]
print(C_n)
# print('Classification Report')
# target_names = ['0', '1', '2', '3']
# print(
#     classification_report(
#         test_generator.classes, y_pred, target_names=target_names))



####################################################################################################################
