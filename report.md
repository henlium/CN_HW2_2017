# Computer Networks HW2 Report

### Program Execution

* Execution

  Use python3 to execute `sender.py`, `agent.py`, and `receiver.py`.
  Configure the settings by modifying the following files. Setting files must be put under the same directory with the programs(multiple copies needed if they run on different machines).


* Settings

  * SENDER.conf

    ```
    [sender's IP]
    [sender's listening port]
    [input file name]
    [timeout] (float in second)
    ```

  * AGENT.conf

    ```
    [agent's IP]
    [agent's listening port] (for sender)
    [agent's listening port] (for receiver)
    [loss rate] (in float)
    ```

  * RECEIVER.conf

    ```
    [receiver's IP]
    [receiver's listening port]
    [output file name]
    ```

### Program Structure

* Sender

  ```mermaid
  graph LR
  S["Start<br>send pkt(0)"]-->B(wait for ACK)
  B -->|"recv ack(n)"| C{n = last pkt?}
  C-->|yes|E(send FIN)
  E-->|time out|E
  E-->|recv FINACK|End
  C-->|no|F(move base to n+1<br>expand window size<br>send not-sent pkt)
  F-->B
  B-->|time out|T("adjust threshold<br>set windows size to 1<br>send pkt(base)")
  T-->B
  ```

* Agent

  ```mermaid
  graph LR
  Start-->A(Wait for pkt)
  A-->|recv data|B{random loss<br>by loss rate}
  B-->|loss|C(drop pkt)
  B-->|else|D(fwd to receiver)
  C-->A
  D-->A
  A-->|recv FIN|D(fwd to receiver)
  F-->A
  A-->|recv ACK or FINACK|E(fwd to sender)
  E-->A
  ```

* Receiver

  ```mermaid
  graph LR
  S[Start<br>seq = 0]-->A(Wait for pkt)
  A-->|recv FIN|E(send FINACK)
  E-->End
  A-->|recv data|F{pkt.seq = seq?}
  F-->|yes|B{buffer full?}
  F-->|no|C(drop packet)
  B-->|yes|G(flush)
  G-->C
  B-->|no|D("pkt to buffer<br>send ack(seq)<br>seq++")
  D-->A
  C-->A
  ```


### Difficulties & Solutions

* Python versions :

  I spent a lot of time debugging sequence number until I found out that `bytes()` in python 2 is just an alias of `str()`.
* Non-blocking socket :

  If I directly set socket as non-blocking, it will raise an error when `recvfrom()` has nothing coming in.I first use `try` and `except` to handle the raised error, and it didn't turn out to be a good method. Later on, I switched back to use blocking IO and `select.select()` to see if there is packet available to be received.