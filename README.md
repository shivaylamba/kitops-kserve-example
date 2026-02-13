# Install KitOps (Kit CLI)
```
cd /root/kserve
tar -xzvf kitops-linux-x86_64.tar.gz
sudo mv kit /usr/local/bin/
kit version
```

# Install Knative Serving
```
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.12.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.12.0/serving-core.yaml
kubectl apply -f https://github.com/knative/net-kourier/releases/download/knative-v1.12.0/kourier.yaml
kubectl patch configmap/config-network --namespace knative-serving --type merge --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'
```
# Verify Knative Installation
```
kubectl get pods -n knative-serving
kubectl get pods -n kourier-system
```
# Install KServe Cluster Resources
```
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.13.0/kserve-cluster-resources.yaml
```
# Prepare the Model
```
cd /root/kserve/iris-sklearn-kit
source .venv/bin/activate
pip install scikit-learn==1.3.2 'numpy<2.0'
python train_iris.py
```
# Package and Push Model with KitOps
```
kit pack . -t jozu.ml/shivaylamba/iris-sklearn:latest
kit push jozu.ml/shivaylamba/iris-sklearn:latest
```
# Deploy KitOps ClusterStorageContainer (if needed)
```
kubectl apply -f kitops-clusterstoragecontainer.yaml
```
# Deploy the InferenceService
```
kubectl apply -f iris-sklearn-inferenceservice.yaml
```
# Wait and Check Status
```
sleep 10
kubectl get inferenceservices
kubectl get pods -l serving.kserve.io/inferenceservice=sklearn-iris
kubectl get ksvc
```
# Test with kubectl run curl-test
```
kubectl run curl-test --rm -it --image=curlimages/curl:8.8.0 --restart=Never -- \
  curl -s -H "Content-Type: application/json" \
  http://sklearn-iris-predictor.default.svc.cluster.local/v1/models/sklearn-iris:predict \
  -d '{"instances": [[5.1, 3.5, 1.4, 0.2], [6.2, 3.4, 5.4, 2.3]]}'
```
