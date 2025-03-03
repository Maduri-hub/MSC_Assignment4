from m5.objects import *

# Create the system
system = System()

# Define the clock for the system
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '2GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Define the CPU (simple pipeline)
system.cpu = TimingSimpleCPU()

# Define the memory (for example, a simple DDR3)
system.mem_mode = 'timing'  # 'atomic' for faster simulations
system.mem_ranges = [AddrRange('512MB')]

# Connect the CPU to the memory
system.membus = SystemXBar()

# Create and connect the memory controller
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Connect the CPU to the memory bus
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

# Set up the system to run a simple workload
system.system_port = system.membus.slave

# Simple branch predictor
system.cpu.branchPred = BPredSimple()

system.cpu = TimingSimpleCPU()

system.cpu.createThreads()
system.cpu.numThreads = 2 

# Instantiate the root of the simulation
root = Root(full_system = False, system = system)

# Collect statistics
print(f"Instructions completed: {system.cpu.stats.numInsts}")
print(f"Cycles taken: {system.cpu.stats.numCycles}")
throughput = system.cpu.stats.numInsts / system.cpu.stats.numCycles
latency = system.cpu.stats.numCycles / system.cpu.stats.numInsts

# Run the simulation
m5.instantiate()
exit_event = m5.simulate()


print(f"Throughput: {throughput} instructions/cycle")
print(f"Latency: {latency} cycles/instruction")


