from odoo import fields,models,api



# import cv2
# import face_recognition



class Img(models.Model):
    _name ='img.module'
    _description = 'that tack a pic and create a new record'

    name=fields.Many2one('first.module','name')
    date_of_birth=fields.Date(string='DOB')
    age=fields.Integer(string='Age',help='Write a age')
    
    @api.model
    def default_get(self,fields_list):
        ret=super(Img,self).default_get(list(map(str,self._fields)))
        print(ret)
        ret['name']=9
        ret['age']=10
        print(ret)
        return ret
        


        # employees =self.env['first.module'].search([])
        # known_face_encodings=[]
        # known_face_names=[]
        # for employee in employees:
        # for employee in employees:
        #     known_face_encodings.append(employee.face_encoding)
        #     known_face_names.append(employee.name)
        # cap = cv2.VideoCapture(0)
        # while True:
        #     ret, frame = cap.read()
        #
        #     if not ret:
        #         print("Failed to grab frame")
        #         break
        #
        #     # Convert the frame from BGR to RGB
        #     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     print(rgb_frame)
        #     print(type(rgb_frame))
        #     # Find all face locations and encodings in the current frame
        #     face_locations = face_recognition.face_locations(rgb_frame)
        #     print(face_locations)
        #     print(type(face_locations))
        #     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        #     print(type(face_encodings))
        #     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        #         matches = face_recognition.compare_faces(known_face_names, face_encoding)
        #         name = "Unknown"
        #
        #         # Use the known face with the smallest distance if a match is found
        #         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        #         best_match_index = face_distances.argmin() if matches else None
        #
        #         if matches and matches[best_match_index]:
        #             name = known_face_names[best_match_index]
        #
        #             # Draw a rectangle around the face and label it
        #         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        #         cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        #
        #         # Display the result
        #     cv2.imshow('Face Recognition', frame)
        #
        #     # Press 'q' to exit the loop
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        #
        # # Release the camera and close the window
        # cap.release()
        # cv2.destroyAllWindows()