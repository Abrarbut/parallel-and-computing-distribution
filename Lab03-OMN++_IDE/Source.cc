#include <omnetpp.h>

using namespace omnetpp;

class Source : public cSimpleModule
{
protected:
    virtual void initialize() override {
        cMessage *msg = new cMessage("packet");
        send(msg, "out");
    }
};

Define_Module(Source);
