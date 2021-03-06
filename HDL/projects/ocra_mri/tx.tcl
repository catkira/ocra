# Create a pin for the 2MHz clock
# create_bd_pin -dir I clk_2MHz

# Create xlslice
cell xilinx.com:ip:xlslice:1.0 slice_0 {
  DIN_WIDTH 8 DIN_FROM 0 DIN_TO 0 DOUT_WIDTH 1
}

# Create xlslice
cell xilinx.com:ip:xlslice:1.0 slice_1 {
  DIN_WIDTH 32 DIN_FROM 15 DIN_TO 0 DOUT_WIDTH 16
}

# Create blk_mem_gen
cell xilinx.com:ip:blk_mem_gen:8.4 bram_0 {
  MEMORY_TYPE True_Dual_Port_RAM
  USE_BRAM_BLOCK Stand_Alone
  WRITE_WIDTH_A 32
  WRITE_DEPTH_A 16384
  WRITE_WIDTH_B 32
  ENABLE_A Always_Enabled
  ENABLE_B Always_Enabled
  REGISTER_PORTB_OUTPUT_OF_MEMORY_PRIMITIVES false
}

# Create axi_bram_writer
cell pavel-demin:user:axi_bram_writer:1.0 writer_0 {
  AXI_DATA_WIDTH 32
  AXI_ADDR_WIDTH 32
  BRAM_DATA_WIDTH 32
  BRAM_ADDR_WIDTH 14
} {
  BRAM_PORTA bram_0/BRAM_PORTA
  aresetn /rst_0/peripheral_aresetn
}

# Create axis_bram_reader
cell open-mri:user:axis_segmented_bram_reader:1.0 reader_0 {
  AXIS_TDATA_WIDTH 32
  BRAM_DATA_WIDTH 32
  BRAM_ADDR_WIDTH 14
  CONTINUOUS FALSE
} {
  BRAM_PORTA bram_0/BRAM_PORTB
  cfg_data slice_1/Dout
  aclk /pll_0/clk_out1
  aresetn slice_0/Dout
}

# Create axis_zeroer
cell pavel-demin:user:axis_zeroer:1.0 zeroer_0 {
  AXIS_TDATA_WIDTH 32
} {
  S_AXIS reader_0/M_AXIS
  aclk /pll_0/clk_out1
}

# Create the interpolator
cell pavel-demin:user:axis_interpolator:1.0 axis_interpolator_0 {
    AXIS_TDATA_WIDTH 32
} {
    S_AXIS zeroer_0/M_AXIS
    aclk /pll_0/clk_out1
    aresetn /micro_sequencer/hf_reset
}

# cell xilinx.com:ip:cmpy:6.0 mult_0 {
  # FLOWCONTROL NonBlocking
  # APORTWIDTH.VALUE_SRC USER
  # BPORTWIDTH.VALUE_SRC USER
  # APORTWIDTH 16
  # BPORTWIDTH 24
  # OUTPUTWIDTH 41
# } {
  # S_AXIS_A axis_interpolator_0/M_AXIS
  # aclk /pll_0/clk_out1
# }

cell open-mri:user:complex_multiplier:1.0 mult_0 {
  OPERAND_WIDTH_A 16
  OPERAND_WIDTH_B 24
  OPERAND_WIDTH_OUT 16
  BLOCKING 0
  STAGES 3
  TRUNCATE 1
} {
  S_AXIS_A axis_interpolator_0/M_AXIS
  aclk /pll_0/clk_out1
  aresetn /micro_sequencer/hf_reset  
}

# extract the real component of the product using a broadcaster in to I and Q
# a simpler alternative would be to use a axis_subset_converter
cell xilinx.com:ip:axis_subset_converter:1.1 real_0 {
    S_TDATA_NUM_BYTES.VALUE_SRC USER
    M_TDATA_NUM_BYTES.VALUE_SRC USER
    S_TDATA_NUM_BYTES 4
    M_TDATA_NUM_BYTES 2
    TDATA_REMAP {tdata[15:0]}
} {
    S_AXIS mult_0/M_AXIS_DOUT
    aclk /pll_0/clk_out1
    aresetn /micro_sequencer/hf_reset
}