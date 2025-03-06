from ns import ns
from ctypes import c_int, c_bool
import sys
import random

#Parameters
numVehicles = 2
defaultXSpeed = 0.0
defaultYSpeed = 0.0
gridWidth = 3
xPositions = [0] * numVehicles
yPositions = [0] * numVehicles
#Protocol, 0 is DSRC and 1 is C-V2X
cV2x = False


ns.LogComponentEnable("UdpEchoClientApplication", ns.LOG_LEVEL_INFO)
ns.LogComponentEnable("UdpEchoServerApplication", ns.LOG_LEVEL_INFO)

#Setting up vehicles
vehicles = ns.NodeContainer()
vehicles.Create(numVehicles)


if not cV2x:
    #Right now, I'm implementing DSRC with a normal wifi connection
    # nWifi = c_int(3)

    # wifiStaNodes = ns.network.NodeContainer()
    # wifiStaNodes.Create(nWifi.value)

    channel = ns.YansWifiChannelHelper.Default()
    phy = ns.YansWifiPhyHelper()
    phy.SetChannel(channel.Create())

    mac = ns.WifiMacHelper()
    ssid = ns.Ssid ("ns-3-ssid")

    wifi = ns.WifiHelper()

    mac.SetType ("ns3::StaWifiMac", "Ssid", ns.SsidValue(ssid), "ActiveProbing", ns.BooleanValue(False))
    vehicleDevices = wifi.Install(phy, mac, vehicles)


if cV2x:
    pass


#Setting up mobility (positions and speeds of vehicles)
mobility = ns.MobilityHelper()
mobility.SetPositionAllocator("ns3::GridPositionAllocator", "MinX", ns.DoubleValue(0.0),
                              "MinY", ns.DoubleValue (0.0), "DeltaX", ns.DoubleValue(defaultXSpeed), "DeltaY", ns.DoubleValue(defaultYSpeed),
                              "GridWidth", ns.UintegerValue(gridWidth), "LayoutType", ns.StringValue("RowFirst"))
mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
mobility.Install(vehicles)


stack = ns.InternetStackHelper()

stack.Install(vehicles)

address = ns.Ipv4AddressHelper()
address.SetBase(ns.Ipv4Address("10.1.1.0"), ns.Ipv4Mask("255.255.255.0"))

vehicleInterfaces = address.Assign(vehicleDevices)

echoServer = ns.UdpEchoServerHelper(9)

serverApps = echoServer.Install(vehicles.Get(numVehicles - 1))
serverApps.Start(ns.Seconds(1.0))
serverApps.Stop(ns.Seconds(10.0))

address = vehicleInterfaces.GetAddress(1).ConvertTo()
echoClient = ns.UdpEchoClientHelper(address, 9)
echoClient.SetAttribute("MaxPackets", ns.UintegerValue(1))
echoClient.SetAttribute("Interval", ns.TimeValue(ns.Seconds(1)))
echoClient.SetAttribute("PacketSize", ns.UintegerValue(1024))

clientApps = echoClient.Install(vehicles.Get(0))
clientApps.Start(ns.Seconds(2))
clientApps.Stop(ns.Seconds(10))

    
# Run the simulation
ns.Simulator.Stop(ns.Seconds(11.0)) # Added simulation stop time
ns.Simulator.Run()
ns.Simulator.Destroy()
