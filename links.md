### Links prometheus
- https://www.airplane.dev/blog/prometheus-exporters
- https://medium.com/teamzerolabs/15-steps-to-write-an-application-prometheus-exporter-in-go-9746b4520e26
- https://trstringer.com/quick-and-easy-prometheus-exporter/

### Links Portainer
- https://portainer.delorenzo.mobi/#!/home
- https://app.swaggerhub.com/apis/portainer/portainer-ee/2.18.3
- https://docs.portainer.io/api/examples

### Links tools
- https://prometheus.io/
- https://grafana.com/

```
API_KEY='ptr_ZZjjmWCiS5YOJcpCd3xIcpLImTwO2LxWNMsWByGJ0jw='
curl -X GET --header 'Content-Type: application/json' --header "x-api-key: $API_KEY" --url 'https://portainer.delorenzo.mobi/api/endpoints/2/docker/containers/974a77279b0e44d3ceda9975081e7fd2d1ac24c92755b1c5dfb74163e15c2cb5/json' | jq
```