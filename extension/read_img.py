
import cv2
import numpy as np
import extension.anti_word_guess as anti_word_guess
shape_5 = (160,136)
shape_6 = (184,160)
shape_7 = (208,184)
first_pixel = (10,10)
step_lenth = 19
gap_lenth = 5

letters = {
    'a' : cv2.imread('letters/A.jpg',cv2.IMREAD_GRAYSCALE),
    'b' : cv2.imread('letters/B.jpg',cv2.IMREAD_GRAYSCALE),
    'c' : cv2.imread('letters/C.jpg',cv2.IMREAD_GRAYSCALE),
    'd' : cv2.imread('letters/D.jpg',cv2.IMREAD_GRAYSCALE),
    'e' : cv2.imread('letters/E.jpg',cv2.IMREAD_GRAYSCALE),
    'f' : cv2.imread('letters/F.jpg',cv2.IMREAD_GRAYSCALE),
    'g' : cv2.imread('letters/G.jpg',cv2.IMREAD_GRAYSCALE),
    'h' : cv2.imread('letters/H.jpg',cv2.IMREAD_GRAYSCALE),
    'i' : cv2.imread('letters/I.jpg',cv2.IMREAD_GRAYSCALE),
    'j' : cv2.imread('letters/J.jpg',cv2.IMREAD_GRAYSCALE),
    'k' : cv2.imread('letters/K.jpg',cv2.IMREAD_GRAYSCALE),
    'l' : cv2.imread('letters/L.jpg',cv2.IMREAD_GRAYSCALE),
    'm' : cv2.imread('letters/M.jpg',cv2.IMREAD_GRAYSCALE),
    'n' : cv2.imread('letters/N.jpg',cv2.IMREAD_GRAYSCALE),
    'o' : cv2.imread('letters/O.jpg',cv2.IMREAD_GRAYSCALE),
    'p' : cv2.imread('letters/P.jpg',cv2.IMREAD_GRAYSCALE),
    'q' : cv2.imread('letters/Q.jpg',cv2.IMREAD_GRAYSCALE),
    'r' : cv2.imread('letters/R.jpg',cv2.IMREAD_GRAYSCALE),
    's' : cv2.imread('letters/S.jpg',cv2.IMREAD_GRAYSCALE),
    't' : cv2.imread('letters/T.jpg',cv2.IMREAD_GRAYSCALE),
    'u' : cv2.imread('letters/U.jpg',cv2.IMREAD_GRAYSCALE),
    'v' : cv2.imread('letters/V.jpg',cv2.IMREAD_GRAYSCALE),
    'w' : cv2.imread('letters/W.jpg',cv2.IMREAD_GRAYSCALE),
    'x' : cv2.imread('letters/X.jpg',cv2.IMREAD_GRAYSCALE),
    'y' : cv2.imread('letters/Y.jpg',cv2.IMREAD_GRAYSCALE),
    'z' : cv2.imread('letters/Z.jpg',cv2.IMREAD_GRAYSCALE),
}


def get_color(img:cv2.Mat):
    summ = 0
    for x in range(0,5):
        for y in range(0,5):
            summ += img[x][y]
    colors = {
        'yellow' : 4500,
        'green' : 3700,
        'gray' : 3000,
        'white' : 6000
    }
    min = 10000
    for color in colors:
        if abs(colors[color] - summ) < min:
            min = abs(colors[color] - summ)
            res = color
    return res

def get_letters(img:cv2.Mat):
    min = 1000000
    cv2.threshold(img,200,255,cv2.THRESH_BINARY,img)
    for key in letters:
        tmp = cv2.absdiff(img, letters[key])
        if np.sum(tmp) < min:
            min = np.sum(tmp)
            letter = key

    return letter
        
def get_shape(shape):
    if shape == shape_5:
        return 5
    elif shape == shape_6:
        return 6
    elif shape == shape_7:
        return 7

def divice_into_pieces(img:cv2.Mat):
    shape = get_shape(img.shape)
    pieces = [[] for i in range(shape+1)]
    for i in range(shape+1):
        for j in range(shape):
            y0 = first_pixel[1] + j * step_lenth + j * gap_lenth
            y1 = y0 + step_lenth
            x0 = first_pixel[0] + i * step_lenth + i * gap_lenth
            x1 = x0 + step_lenth
            pieces[i].append(img[x0:x1,y0:y1])
    return pieces

def get_info(img):
    pieces = divice_into_pieces(img)
    word_len = get_shape(img.shape)
    letter_in_word = ''
    letter_not_in_word = ''
    letter_in_right_index = []
    letter_in_wrong_index = []
    for i in range(len(pieces)):
        for j in range(len(pieces[i])):
            color = get_color(pieces[i][j])
            if color == 'white':
                continue
            else:
                litter = get_letters(pieces[i][j])
                
            if color == 'yellow':
                if litter not in letter_in_word:
                    letter_in_word += litter
                if (litter,j) not in letter_in_right_index:
                    letter_in_right_index.append((litter,j+1))
            elif color == 'green':
                if litter not in letter_in_word:
                    letter_in_word += litter
                if (litter,j) not in letter_in_wrong_index:
                    letter_in_wrong_index.append((litter,j+1))
            elif color == 'gray':
                if litter not in letter_not_in_word:
                    letter_not_in_word += litter
    words = anti_word_guess.words
    
    words = [word for word in words if len(word) == word_len]
    
    if letter_in_word:
        words = anti_word_guess.letter_in_word(words,letter_in_word,True)
    if letter_not_in_word:
        words = anti_word_guess.letter_in_word(words,letter_not_in_word,False)  

    if letter_in_wrong_index:
        words = anti_word_guess.right_index(words,letter_in_wrong_index,True)
    if letter_in_right_index:
        words = anti_word_guess.right_index(words,letter_in_right_index,False)
    print(words)
    if len(words) >20:
        words = anti_word_guess.recommand_words(words)
        if len(words) > 20:
            words = words[:20]
            
    return words
