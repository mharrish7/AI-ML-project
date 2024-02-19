# Create a mesh topology with 4 nodes
set ns [new Simulator]
set tracefile [open "mesh_topology.tr" w]
$ns trace-all $tracefile

# Define node properties
set node_bw 1Mb  ;# Link bandwidth
set node_delay 10ms  ;# Link delay

# Create nodes
set node_num 4
for {set i 0} {$i < $node_num} {incr i} {
    set node($i) [$ns node]
}

# Create links with loss model (for packet drops)
for {set i 0} {$i < $node_num} {incr i} {
    for {set j 0} {$j < $node_num} {incr j} {
        if {$i != $j} {
            set link($i,$j) [$ns duplex-link $node($i) $node($j) $node_bw $node_delay DropTail]
            set q_limit($i,$j) 10
            $link($i,$j) queue-limit $q_limit($i,$j)  ;# Set queue limit
            $link($i,$j) drop-target [new Agent/Null]
            $link($i,$j) queue-sample 0.1  ;# Set packet drop probability
            $ns at 0.0 "\$link($i,$j) drop-target drop 0"
        }
    }
}

# Generate traffic
set udp [new Agent/UDP]
$ns attach-agent $node(0) $udp
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set rate 1Mb  ;# Set traffic rate
$cbr set packetSize 500  ;# Set packet size
$cbr set interval 0.01  ;# Set packet interval
$ns at 0.1 "\$cbr start"
$ns at 4.0 "\$cbr stop"

# Define simulation end time
set sim_end_time 5.0
$ns at $sim_end_time "finish"

# Define procedure to finish simulation
proc finish {} {
    global ns tracefile
    $ns flush-trace
    close $tracefile
    puts "Simulation completed"
    exit 0
}

# Run the simulation
$ns run
