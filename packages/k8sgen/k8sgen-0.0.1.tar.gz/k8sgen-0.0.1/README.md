# k8sGen
---
## About
k8sGen was developed out of a need for a framework to enable to creation of kubernetes manifests based off the objects that are required, not a template.  Popular templating tools, like [Helm](https://helm.sh), is excellent in that it allows for values to be swapped into existing structures but becomes clunky when a large amount of customization is required on the Kubernetes-object level. Furthermore, Amazon's [cdk8s](https://cdk8s.io) excels at providing a more developer-freidnly way to generate manifests, but isn't so friendly to an application that needs to generate them for a user.  This is where k8sGen comes in.  By providing accessible Python classes for Kubernetes objects and the components, k8sGen enables applications to quickly build manifests based off of user-supplied configuration for use in installation guides and more.


Documentation for k8sGen is available [here](https://k8sgen.readthedocs.io/en/latest/)


This project is maintained by John Carter with the support of [ModelOp](http://modelop.com)