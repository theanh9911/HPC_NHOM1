from locust import HttpUser, task, between

IMG_PATH = r"C:\Users\The Anh\OneDrive\Máy tính\Project\Data\training-images\train-images\000d70ebbab2de0be64c4fb313eae62835e26ee7cd2711f5f23f14b652be949e.jpg"  # Đường dẫn tương đối tới file ảnh test

class PneumoniaUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict(self):
        with open(IMG_PATH, 'rb') as f:
            files = {'files': (IMG_PATH, f, 'image/jpeg')}
            self.client.post('/predict', files=files) 