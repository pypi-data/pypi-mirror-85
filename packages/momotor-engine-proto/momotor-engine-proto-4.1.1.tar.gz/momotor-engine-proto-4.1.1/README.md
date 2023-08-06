This package is a part of [Momotor](https://momotor.org/), a tool for automated processing of digital content. 

Momotor accepts digital content as a product bundle and generates a result bundle from this product under 
control of a recipe bundle. 

Momotor is like a continuous integration system, but broader in scope. The 
type of content that Momotor can process is not restricted; each recipe may impose its own constraints. 
One application of Momotor in an educational setting is the automatic generation of feedback on work submitted 
for programming assignments.

---

The `momotor-engine-proto` package provides the Momotor RPC protocol for communication between the Momotor 
broker and clients, and also for the communication between the Momotor broker and workers.

The protocol uses the Google RPC (gRPC) protocol.
