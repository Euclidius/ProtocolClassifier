import pyshark
import sys

# validate arguments
input_file = sys.argv[1][:-1]
output_file = sys.argv[2][:-1]
stop_index = int(sys.argv[3])

class Package:
    destination_ip: str
    source_ip: str
    destination_port: str
    source_port: str
    packet_len: str
    payload: str

    def __init__(self, dip, sip, dop, sop, plen):
        self.destination_ip = dip
        self.source_ip = sip
        self.destination_port = dop
        self.source_port = sop
        self.packet_len = plen
        self.payload = ''


streams: dict[int, list[Package]] = {}


def main():
    cap = pyshark.FileCapture(input_file)
    for packet in cap:
        stream_id = packet.tcp.stream
        index = streams.get(stream_id)
        if index:
            if len(index) == stop_index:
                continue

        package = Package(
            packet.ip.src,
            packet.tcp.srcport,
            packet.ip.dst,
            packet.tcp.dstport,
            int(packet.tcp.hdr_len) + int(packet.tcp.len)
        )
        if hasattr(packet.tcp, 'payload'):
            package.payload = packet.tcp.payload.replace(':', '')

        stream_id = packet.tcp.stream
        print(stream_id)
        if not streams.get(stream_id):
            streams[stream_id] = [package]
        elif len(streams[stream_id]) < stop_index:
            streams[stream_id].append(package)
        else:
            continue  # remove lol

    valid_streams = {}
    for stream_id in streams.keys():
        if len(streams[stream_id]) == stop_index:
            valid_streams[stream_id] = streams[stream_id]

    output = open(f'{output_file}', 'w')
    column_index = 'n,src_ip,sport,dst_ip,dport,proto'
    for i in range(stop_index):
        column_index += f',payload_bytes_{i}'
    for i in range(stop_index):
        column_index += f',direction_{i}'
    for i in range(stop_index):
        column_index += f',pkt_len_{i}'
    output.write(column_index + '\n')

    for stream_id in valid_streams.keys():
        stream = streams[stream_id]
        output.write(f'{stream_id},{stream[0].source_ip},{stream[0].source_port},'
                     f'{stream[0].destination_ip},{stream[0].destination_port},6')
        for packet in streams[stream_id]:
            output.write(f',{packet.payload}')
        for packet in streams[stream_id]:
            if packet.source_ip == streams[stream_id][0].source_ip:
                output.write(f',1')
            else:
                output.write(f',-1')
        for packet in streams[stream_id]:
            output.write(f',{packet.packet_len}')
        output.write('\n')
    output.close()

if __name__ == '__main__':
    main()
