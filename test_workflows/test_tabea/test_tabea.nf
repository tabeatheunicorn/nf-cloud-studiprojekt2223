#!/home/tabeatheunicorn/nf-cloud-studiprojekt2223/nextflow
params.in = "hello"
 
/*
 * Split a fasta file into multiple files
 */
process echoSequence {
 
    input:
    val x
 
    exec:
    println "Echo: $x"
}

process waitNSeconds {
    input:
    val x

    """
    sleep $x
    """
}
 
/*
 * Define the workflow
 */
workflow {
    Channel.of(10, 8, 4) | waitNSeconds
    Channel.of('a', 'b', 'c') | echoSequence
}