import numpy as np
import cv2
    # biblioteca OpenCV que lida com imagens e vídeos

def libras(*word):
# a função libras recebe quantas palavras forem definidas
# exemplo: librasfunction.libras('banana', 'fruta')

    n = len(word)
    i = 0

    def split(word): 
    # função que separa a palavra letra por letra
        return [char for char in word]

    while (i < n):
    #laço que separa palavra por palavra

        try:
        # laço que mostra o vídeo da palavra existente na biblioteca

            path = 'videos/' + word[i] + '.mp4'
            f = open(path)
            # verificação da existência do vídeo
            f.close()
            print('Palavra encontrada.')

            delay = 60

            cap = cv2.VideoCapture(path)

            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    cv2.imshow('Frame', frame)
                    if cv2.waitKey(delay) & 0xFF == ord('q'):
                        break
                else:
                    break
        
        except FileNotFoundError:
        # laço que mostra o vídeo da palavra não existente na biblioteca.
        # nesse caso, serão mostrados pequenos vídeos que soletram a palavra

            print('Palavra não encontrada.')

            m = len(word[i])
            j = 0
            delay = 30

            while (j < m):

                letter = split(word[i])
                path = 'videos/alfabeto/' + letter[j] + '.mp4'
                
                cap = cv2.VideoCapture(path)

                while(cap.isOpened()):
                    ret, frame = cap.read()          
                    if ret == True:
                        cv2.imshow('Frame', frame)
                        if cv2.waitKey(delay) & 0xFF == ord('q'):
                            break
                    else:
                        break

                j = j + 1
        i = i + 1

    cap.release()
    cv2.destroyAllWindows()