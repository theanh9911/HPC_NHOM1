# Hướng dẫn setup Docker Swarm nhiều node (1 manager, 2 worker)

## 1. Chuẩn bị
- Cài Docker trên tất cả các máy (manager, worker).
- Đảm bảo các máy cùng mạng LAN hoặc có thể ping nhau.

## 2. Khởi tạo Swarm trên máy manager
```bash
# Trên máy manager
sudo docker swarm init --advertise-addr <IP_MANAGER>
```
Sau khi chạy, sẽ hiện ra lệnh join cho worker, ví dụ:
```
docker swarm join --token <TOKEN> <IP_MANAGER>:2377
```

## 3. Thêm worker vào swarm
- Trên mỗi máy worker, chạy lệnh join ở trên:
```bash
sudo docker swarm join --token <TOKEN> <IP_MANAGER>:2377
```

## 4. Kiểm tra node
- Trên manager:
```bash
sudo docker node ls
```

## 5. Deploy stack
- Trên manager:
```bash
sudo docker stack deploy -c docker-compose.yml pneumonia
```

## 6. Kiểm tra service
```bash
sudo docker service ls
sudo docker service ps pneumonia_pneumonia-api
```

## 7. Scale số lượng replicas (nếu muốn)
```bash
sudo docker service scale pneumonia_pneumonia-api=5
```

## 8. Xem log container
```bash
sudo docker service logs pneumonia_pneumonia-api
```

## 9. Gỡ node khỏi swarm (nếu cần)
- Trên worker:
```bash
sudo docker swarm leave
```
- Trên manager:
```bash
sudo docker node rm <NODE_ID>
``` 