#include <omnetpp.h>

using namespace omnetpp;

class LoadBalancer : public cSimpleModule
{
protected:
    virtual void handleMessage(cMessage *msg) override {
        int choice = intuniform(0, 1);
        send(msg, "out", choice);
    }
};

Define_Module(LoadBalancer);
