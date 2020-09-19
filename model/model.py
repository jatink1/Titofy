def createModelFeedForward(X, y):
    
    rows, songs, num_features = X.shape
    
    num_features = y.shape[1]
    
    out_dim = y.shape[1] # X.shape[1] should be equal to y.shape[1]
    model = Sequential([Dense(64, input_shape = (songs, num_features), activation='relu'),
                          Dense(32, activation='relu'),
                          Dense(16, activation='relu'),
                          Flatten(),
                          Dense(num_features, activation="sigmoid")])
    
    model.compile(optimizer='adam', loss = "binary_crossentropy", metrics = ["accuracy"])
    
    print(model.summary())
    
    return model

model = createModelFeedForward(X, y)

#model.fit(X, y, epochs = 20, batch_size = 128) #DO NOT RUN THIS