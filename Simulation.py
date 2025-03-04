from ns import ns
import sys
import random

#Parameters
numVehicles = 2
defaultXSpeed = 0.0
defaultYSpeed = 0.0
gridWidth = 3
xPositions = [0] * numVehicles
yPositions = [0] * numVehicles


#Setting up vehicles
nodes = ns.network.NodeContainer()
nodes.Create(numVehicles)

#Setting up mobility (positions and speeds of vehicles)
mobility = ns.mobility.MobilityHelper()
mobility.SetPositionAllocator("ns3::GridPositionAllocator", "MinX", ns.core.DoubleValue(0.0),
                              "MinY", ns.core.DoubleValue (0.0), "DeltaX", ns.core.DoubleValue(defaultXSpeed), "DeltaY", ns.core.DoubleValue(defaultYSpeed),
                              "GridWidth", ns.core.UintegerValue(gridWidth), "LayoutType", ns.core.StringValue("RowFirst"))
mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
mobility.Install(nodes)