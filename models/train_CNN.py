import tensorflow as tf

tf.random.set_seed(1234)

batch_size = 32
img_height = 100
img_width = 100

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory="Spectograms",
    labels="inferred",
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    color_mode='grayscale'
)

valid_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory="Spectograms",
    labels="inferred",
    validation_split=0.2,
    subset= "validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    color_mode='grayscale'
)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().cache().prefetch(buffer_size=AUTOTUNE)
val_ds = valid_ds.cache().cache().prefetch(buffer_size=AUTOTUNE)

model = tf.keras.models.Sequential([
    tf.keras.layers.Rescaling(1./255, input_shape=(img_height, img_width, 1)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(18)
])


model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=['acc'])

my_callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=2),
    tf.keras.callbacks.ModelCheckpoint(
        filepath='models/model.{epoch:02d}-{val_loss:.2f}.h5',
        save_best_only=True,
        monitor='val_loss',
        mode='min'
    ),
    tf.keras.callbacks.TensorBoard(log_dir='./logs'),
]

model.fit(train_ds, 
          epochs=10, 
          validation_data=val_ds,
          callbacks=my_callbacks)