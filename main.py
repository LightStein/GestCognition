''
ჯგუფის ნომერი: 4
პროექტის თემა: Hand Gesture Recognition using Python and OpenCV
ჯგუფის წევრები: ელენე კვარაცხელია, ანრი გიორგანაშვილი, ანა ონიანაშვილი, ანა ბერიშვილი

'''

import cv2  # გამოსახულების მისაღებად
import numpy as np # მატრიცული ინფორმაციის შენახვა დამუშავებისთვის
import math # მათემატიკური გამოთვლების საწარმოებლად


#   ვააქტიურებთ კამერას
capture = cv2.VideoCapture(0) # 0 არის კამერის იდენტიფიკატორი (თუ მეორე კამერაც გვაქვს 1-ანს ჩავწერთ)

# isOpened აბრუნებს Boolean-ს (გააქტიურებულია თუ არა კამერა)
while capture.isOpened():

    # თუ შემდეგი Frame არსებობს ret იქნება True (და არაფერში არ ვიყენებთ, უბრალოდ 2 პარამეტრს აბრუნებს read())
    # frame კი კადრია
    ret, frame = capture.read()

    #   ეკრანზე გამოსახულების რაღაც ნაწილში უნდა მივუთითოთ ადგილი სადაც ხელი უნდა შევიტანოთ
    #   კოორდ1, კოორდ2 მოპირისპირე კუთხეებია
    #   fraction - კოორდინატში შეყვანილ რიცხვში მძიმის მერე სიზუსტე (ჩვენ არ გვაქვს ათწილადი ამიტომ 0-ს ვწერთ)
    #                     კოორდ 1    კოორდ 2  ფერი (R,G,B) # fraction
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)

    #   მიღებული კადრიდან ვჭრით მხოლოდ იმ ადგილს სადაც ხელი ფიქსირდება
    crop_image = frame[100:300, 100:300]

    #   ვაბუნდოვნებთ კადრს, რომ მარტივი დასამუშავებელი იყოს
    #                         source     x, y გაბუნდოვნების კოეფიციენტები
    blur = cv2.GaussianBlur(crop_image, (3, 3), 0)  # 0 = BORDER_CONSTANT BorderType რომელიც ჩარჩოში სვავს გამოსახულებას

    #   BLUE-GREEN-RED -> HUE-SATURATION-VALUE  Colorspace Convertion
    #   BGR/RGB ფერების მოდელთან შედარებით HSV-ში ფერების Range-ის განსაზღვრა უფრო მარტივია
    #   ამიტომ იყენებს OpenCV HSV-მოდელს კადრებში ობიექტების აღსაქმელად
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #   ვქმნით მასკას (ანუ ვათეთრებთ იმ ობიექტს რომელიც გვჭირდება და დანარჩენს ვაშავებთ)
    #   ვუთითებთ კანის ფერის Range-ს   საწყისი  colorizer.org   საბოლოო
    mask2 = cv2.inRange(hsv, np.array([2, 0, 0]), np.array([20, 255, 255]))
    
    #   კერნელის ინიციალიზაცია მორფოლოგიური ტრანსფორმაციისთვის
    #   შეამჩნევდით რომ ვიყენებთ numpy-ს (np) რითიც ვქმნით 5x5 მატრიცას სადაც ყველა წევრი არის 1
    

    #   მასკის შექმნისას (მე-40 ხაზი) რა თქმა უნდა ხელის გარდა ფონზე სხვა რაღაცეებიც შეიძლება გათეთრდეს
    #   იმიტომ რომ კანის ფერის range-ში სხვა ობიექტების ფერიც შეიძლება იყოს
    #   ანუ გამოსახულებაში გვექნება "ხმაური" ( background noise )
    #   იმისთვის რომ მოვიშოროთ ეს "ხმაური" მორფოლოგიური ტრანსფორმაცია გვჭირდება
    #   გვაქვს მრავალი მორფ.ტრანსფორმაცია მაგ: ეროზია(გამოსახულებას გარედან ჭამს), Opening და სხვა
    #   https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
    #               ყველა გამოსახულებას გაასქელებს
    dilation = cv2.dilate(mask2, kernel, iterations=1)  # iterations - რამდენჯერ უნდა გადაატაროს ეფექტი
    #              და ეროზიისას ზედმეტი წერტილები დაიკარგება
    erosion = cv2.erode(dilation, kernel, iterations=1)
    
        filtered = cv2.GaussianBlur(erosion, (3, 3), 0)

    #   https://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
    #   thresholding-ისას პიქსელის მნიშვნელობა თუ მეტია ზღვარზე მას გადაეწერება
    #   ახალი მნიშვნელობა (A) თუ ნაკლებია (B)
    #                           src    ზღვარი   A   B
    ret, thresh = cv2.threshold(filtered, 127, 255, 0)

    #   გამოვიტანოთ დამუშავებული გამოსახულება

    cv2.imshow("Thresholded", thresh)

    #   გამოსახულებაში ვპოულობთ კონტურებს
    #   RETR_TREE პოულობს კონტურებს კონტურებში (შვილებს, შვილიშვილებს და ა.შ)
    #   CHAIN_APPROX_SIMPLE კი ამარტივებს კონტურებს (გადაბმის წერტილებს ნიშნავს მარტო)
    #                                        src
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:
        # ვპოულობთ ყველაზე დიდი ფართობის მქონე კონტურს 
        # (კადრში ყველაზე დიდი ობიექტი ჩვენი ხელია)
        contour = max(contours, key=lambda x: cv2.contourArea(x))

        #   ვქმნით ჩარჩოს რომელიც ხელის ობიექტს შემოეკვრება
        #   x, y - ზედა, მარცხენა წერტილის კოორდინატებია
        #   w - სიგანე, h - სიმაღლე
        x, y, w, h = cv2.boundingRect(contour)
        #   A და B ერთმანეთის საპირისპირო კუთხეებია
        #   0 - მძიმის მერე სიზუსტე
        #                           A           B        ჩარჩოს ფერი   
        cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)

        #   ხელზე გარსშემორტყმული კონტურის მისაღებად ვიყენებთ convexHull-ს
        hull = cv2.convexHull(contour)

        #   ვხატავთ კონტურებს ხელის გარშემო

        #   ვქმნით ცარიელ სურათს (0-ებით გავსებულ მატრიცას)
        #                   200, 200, 3(RGB), არაუარყოფითი int 0-255
        drawing = np.zeros(crop_image.shape, np.uint8)
        #   drawing-ში ჩახატავს კონტურებს, მწვანეს და წითელს
        #   -1 ნიშნავს რომ ყველა კონტური დაიხატოს
        #   სისქე თუ >= 0-ზე კონტური იხაზება, თუ არადა შეავსებს ფიგურას
        #                                            BGR      
        cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0) # სისქე
        cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

        #   ვპოულობთ დეფექტებს (კუთხეებს)
        #   https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_contours/py_contours_more_functions/py_contours_more_functions.html
        hull = cv2.convexHull(contour, returnPoints=False)
        
        #   აქ კი მივიღებთ array-ს სადაც თითო მნიშვნელობა გამოიყურება ასე:
        #   [ start point, end point, farthest point, approximate distance to farthest point ]
        defects = cv2.convexityDefects(contour, hull)

	 # კოსინუსების თეორემის გამოყენებით ვითვლით შორეული კუთხეების დახრილობას (თითის წვერებზე მონიშნულ წერტილებზე)
        count_defects = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])

            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

            # თუ კუთხე < 90-ზე კიდეზე ვსავთ წერტილს და ვთვლით დეფექტში
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_image, far, 1, [0, 0, 255], -1)

            cv2.line(crop_image, start, end, [0, 255, 0], 2)

            # დავბეჭდავთ თითების რაოდენობას
        if count_defects == 0:
            cv2.putText(frame, "ONE", (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 2,(255,255,255),2)
        elif count_defects == 1:
            cv2.putText(frame, "TWO", (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 2,(255,255,255), 2)
        elif count_defects == 2:
            cv2.putText(frame, "THREE", (5, 50), cv2.FONT_HERSHEY_TRIPLEX, 2,(255,255,255), 2)
        elif count_defects == 3:
            cv2.putText(frame, "FOUR", (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 2,(255,255,255), 2)
        elif count_defects == 4:
            cv2.putText(frame, "FIVE", (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 2,(255,255,255), 2)
        else:
            pass
    except:
        pass
#   გამოსახულებები გამოგვაქვს ფანჯრებში
   cv2.imshow("Gesture", frame)
   #   ორი გამოსახულება გვერდიგვერდ ერთ ფანჯარაში
   all_image = np.hstack((drawing, crop_image))
   cv2.imshow('Contours', all_image)

   #   თუ დავაწვებით q-ს დაიხუროს პროგრამა
   if cv2.waitKey(1) == ord('q'):
       break

capture.release()
cv2.destroyAllWindows()