# importation of library
import os
from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from scipy.spatial.distance import cosine
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
from mtcnn.mtcnn import MTCNN
import cv2
#img is a folder/datbase containing the picutures of members and visitors
data_visitor_dir = 'img/visitor'
data_test_dir = 'img/test'
data_member_dir = 'img/member'

def cam():
    camera = cv2.VideoCapture(0)
    while True:
        return_value, image = camera.read()
        cv2.imshow('image', image)
        if cv2.waitKey(1)& 0xFF == ord('s'):
            cv2.imwrite('pic.jpg', image)
        break
    camera.release()
    cv2.destroyAllWindows()
    detector = MTCNN()
	# detect faces in the image
    results = detector.detect_faces(image)
	# extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
	# extract the face
    face = image[y1:y2, x1:x2]
	# resize pixels to the model size
    images = Image.fromarray(face)
    required_size = (224, 224)
    images = images.resize(required_size)
    face = [asarray(images)]
    samples = asarray(face, 'float32')
	# prepare the face for the model, e.g. center pixels
    samples = preprocess_input(samples, version=2)
	# create a vggface model
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
	# perform prediction
    img = model.predict(samples)
    return img

data_visitor = [data_visitor_dir +'/'+i for i in os.listdir(data_visitor_dir)]
data_member = [data_member_dir +'/'+i for i in os.listdir(data_member_dir)]
data_test = [data_test_dir +'/'+i for i in os.listdir(data_test_dir)]

# extract a single face from a given photograph
def extract_face(filename, required_size=(224, 224)):
    try:
        # load image from file
        pixels = pyplot.imread(filename)
    	# create the detector, using default weights
        detector = MTCNN()
    	# detect faces in the image
        results = detector.detect_faces(pixels)
    	# extract the bounding box from the first face
        x1, y1, width, height = results[0]['box']
        x2, y2 = x1 + width, y1 + height
    	# extract the face
        face = pixels[y1:y2, x1:x2]
    	# resize pixels to the model size
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        return face_array
    except IndexError:
        print('This function did not detect any face in the picture')
        return None 
# extract faces and calculate face embeddings for a list of photo files
def get_embeddings(filenames):
	# extract faces
    faces = [extract_face(f) for f in filenames]
	# convert into an array of samples
    samples = asarray(faces, 'float32')
	# prepare the face for the model, e.g. center pixels
    samples = preprocess_input(samples, version=2)
	# create a vggface model
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
	# perform prediction
    yhat = model.predict(samples)
    return yhat

# determine if a candidate face is a match for a known face
def is_match(known_embedding, candidate_embedding, thresh=0.5):
    score = cosine(known_embedding, candidate_embedding)
    #print('>(%.3f vs %.3f)' % (score, thresh))
    return score	
# identify known photos
def member():
    # get embeddings file filenames
    embedding = []
    for i in range(len(data_member)):
        mem = [data_member[i] +'/'+k for k in os.listdir(data_member[i])]
        if data_member[i]+'/'+'Thumbs.db' in mem:
            mem.remove(data_member[i]+'/'+'Thumbs.db')
        embeddings2 = get_embeddings(mem)
        embedding.append(embeddings2)
    return embedding
#visitor check
def visitor():
    # get embeddings file filenames
    embeddings = []
    for i in range(len(data_visitor)):
        vis = [data_visitor[i] +'/'+k for k in os.listdir(data_visitor[i])]
        if data_member[i]+'/'+'Thumbs.db' in vis:
            vis.remove(data_member[i]+'/'+'Thumbs.db')
        embeddings2 = get_embeddings(vis)
        embeddings.append(embeddings2)
    return embeddings
#test the embeddings
def check():
    embeddings1 = cam()
    hue = 0
    embed = member()
    for i in range(len(data_member)):
        for j in range(len(embed[i])):
            score = is_match(embed[i][j], embeddings1)
            if score <= 0.5:
                hue += 1
            else:
                hue = hue
        if hue >= 3:
            print('\n')
            print('>face is a MATCH for %s' %(os.listdir(data_member_dir)[i]))
            print('\n')
            chek = 1
            break
    if chek != 1:
        embedd = visitor()
        huet = 0
        for i in range(len(data_visitor)):
            for j in range(len(embedd[i])):
                score = is_match(embedd[i][j], embeddings1)
                if score <= 0.5:
                    huet += 1
                else:
                    huet = huet
            if huet >= 2:
                print('\n')
                print('>face is a MATCH for %s' %(os.listdir(data_visitor_dir)[i]))
                print('\n')
                chek = 2
                break
    if chek != 1 and chek != 2:
        print('NO MATCH for this person!')
