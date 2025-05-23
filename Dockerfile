# Hướng dẫn triển khai ứng dụng Pneumonia Detection trên Minikube/Kubernetes

## Yêu cầu hệ thống

- Docker Desktop
- Minikube
- kubectl
- Python 3.8+
- pip

## Cài đặt môi trường

1. Cài đặt Minikube:
```bash
# Windows (PowerShell với quyền Administrator)
winget install minikube

# Khởi động Minikube
minikube start
minikube start --nodes=3 --cpus=4 --memory=2048 --driver=docker
```

2. Kiểm tra cài đặt:
```bash
minikube status
kubectl version
```

## Các bước triển khai

### 1. Build Docker Image

```bash
# Di chuyển vào thư mục chứa Dockerfile
cd <đường_dẫn_thư_mục_project>

# Build Docker image
docker build -t pneumonia-detection:latest .

# Load image vào Minikube
minikube image load pneumonia-detection:latest
```

### 2. Triển khai trên Kubernetes

```bash
# Áp dụng file deployment
kubectl apply -f pneumonia-deployment.yaml

# Kiểm tra trạng thái deployment
kubectl get deployments
kubectl get pods
kubectl get services
```

### 3. Truy cập ứng dụng

```bash
# Mở port-forward để truy cập ứng dụng
minikube service pneumonia-service
```

## Kiểm tra ứng dụng

1. Mở trình duyệt web  
2. Upload ảnh X-quang để kiểm tra
3. Xem kết quả phân tích

## Load Testing (Tùy chọn)

Để chạy load test với Locust:

```bash
# Cài đặt Locust
pip install locust

# Chạy load test
locust -f locustfile.py --host <link-web>
```

Truy cập http://localhost:8089 để cấu hình và chạy load test.

## Xử lý sự cố

1. Kiểm tra logs của pod:
```bash
kubectl logs <pod_name>
```

2. Kiểm tra trạng thái pod:
```bash
kubectl describe pod <pod_name>
```

3. Khởi động lại deployment nếu cần:
```bash
kubectl rollout restart deployment pneumonia-deployment
```

## Dọn dẹp

```bash
# Xóa deployment
kubectl delete -f pneumonia-deployment.yaml

# Dừng Minikube
minikube stop
```

## Lưu ý

- Đảm bảo Minikube đã được khởi động trước khi triển khai
- Model file (model_5.pth) cần được đặt trong thư mục project
- Các port mặc định: 8000 (ứng dụng), 8089 (Locust)
- Đảm bảo có đủ tài nguyên hệ thống cho Minikube (ít nhất 4GB RAM) 
