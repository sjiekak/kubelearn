# Setup minikube

[Install minikube](https://minikube.sigs.k8s.io/docs/start/)

```sh
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb && rm minikube_latest_amd64.deb
```

minikube will be run in rootless mode using docker driver. We need to [enable delegation](https://github.com/kubernetes/minikube/issues/14871#issuecomment-1232505089)

```sh
sudo mkdir -p /etc/systemd/system/user@.service.d
cat <<EOF | sudo tee /etc/systemd/system/user@.service.d/delegate.conf
[Service]
Delegate=cpu cpuset io memory pids
EOF
sudo systemctl daemon-reload
```
