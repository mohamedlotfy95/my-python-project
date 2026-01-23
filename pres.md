
At the beginning of the research, I had a call with Brend, during which we agreed on the key points that should be considered in the selection of an alternative solution. For example, we decided that both migrations—the NGINX Ingress and the controllers—would be performed at the same time.




### **Why Switch to Gateway API**

The **Ingress API** is Kubernetes’ standard way to handle external HTTP/HTTPS traffic for services. It is widely used and supported, with many Ingress controllers available. Cloud-native tools like **cert-manager** and **ExternalDNS** also work with it.

However, the Ingress API has some limitations:

* **Limited features:** It only handles TLS termination and basic HTTP request routing.
* **Depends on annotations:** Each Ingress controller uses its own extensions, which makes it hard to move configurations between controllers.
* **Weak permission model:** It is not ideal for clusters shared by multiple teams because it doesn’t provide fine-grained access control for load balancing.



The solution must meet the following requirements:

1. Support the same core features as the current Ingress.
2. Be simple to migrate.
3. Ensure long-term support, such as CNCF certification.
4. Be cost-efficient.

Additionally, we considered future strategic points, including:

* AI agent communication support.
* Gateway API support.
* The ability to handle agentic workloads efficiently.

Based on my research, I identified the following options for comparison:

**Alternative Solutions:**

1. Azure Application Gateway Ingress Controller (AGIC) – AKS Only
2. Traefik Ingress Controller
3. HAProxy Ingress Controller
4. Istio Service Mesh
5. Envoy Gateway
6. Kong Ingress Controller
7. Contour (Envoy-based)
8. Emissary-Ingress (formerly Ambassador)
9. Cilium Ingress Controller
10. Kubernetes Gateway API (Native Standard)

Each option can be reviewed individually to assess its pros and cons.

---

**Top Recommendations (focused on RKE2 support):**

RKE2 officially supports Traefik, Cilium, and (until retirement) NGINX Ingress. Traefik has become the preferred and officially supported ingress and gateway option as of August 2024.

Other ingress and gateway solutions, such as Envoy Gateway, Contour, Kong, HAProxy, and Emissary, can be installed manually but are not built into or officially supported by RKE2.

For environments running both AKS and RKE2 that require full Gateway API support, long-term stability, and modern traffic capabilities like AI agent communication, **Traefik in Gateway API mode** is the best choice. It is integrated with RKE2, easy to enable, free, and well-supported by both Rancher and Traefik Labs.

**Other options:**

* **Envoy Gateway:** Strong second choice with excellent Gateway API support and CNCF backing, but requires manual installation and lacks Rancher integration.
* **Cilium Ingress:** Powerful if Cilium is already used as the CNI, but migration requires more effort.
* **Contour:** Reliable, but ranks lower due to manual setup and lack of official Rancher support.
