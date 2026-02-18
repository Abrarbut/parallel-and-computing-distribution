simple Source
{
    gates:
        output out;
}

simple LoadBalancer
{
    gates:
        input in[6];
        output out[2];
}

simple Sink
{
    gates:
        input in;
}

network Lab3
{
    submodules:
        A[6]: Source;
        B: LoadBalancer;
        S[2]: Sink;

    connections:
        for i=0..5 {
            A[i].out --> B.in[i];
        }

        B.out[0] --> S[0].in;
        B.out[1] --> S[1].in;
}
