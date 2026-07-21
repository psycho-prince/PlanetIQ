#include <iostream>
#include <vector>
#include <cstdint>
#include <iomanip>
#include <string>

struct ModbusPacket {
    uint16_t transaction_id;
    uint16_t protocol_id;
    uint16_t length;
    uint8_t unit_id;
    uint8_t function_code;
    std::vector<uint8_t> data;
};

ModbusPacket parseModbusTCP(const std::vector<uint8_t>& packet) {
    ModbusPacket mp;
    if (packet.size() < 8) {
        std::cerr << "Packet too short" << std::endl;
        return mp;
    }
    
    mp.transaction_id = (packet[0] << 8) | packet[1];
    mp.protocol_id = (packet[2] << 8) | packet[3];
    mp.length = (packet[4] << 8) | packet[5];
    mp.unit_id = packet[6];
    mp.function_code = packet[7];
    
    if (packet.size() > 8) {
        mp.data.assign(packet.begin() + 8, packet.end());
    }
    return mp;
}

void printPacket(const ModbusPacket& mp) {
    std::cout << "Modbus Packet:" << std::endl;
    std::cout << "  Transaction ID: 0x" << std::hex << mp.transaction_id << std::dec << std::endl;
    std::cout << "  Protocol ID: " << mp.protocol_id << std::endl;
    std::cout << "  Length: " << mp.length << std::endl;
    std::cout << "  Unit ID: " << (int)mp.unit_id << std::endl;
    std::cout << "  Function Code: 0x" << std::hex << (int)mp.function_code << std::dec << std::endl;
    std::cout << "  Data: ";
    for (uint8_t b : mp.data) {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)b << " ";
    }
    std::cout << std::dec << std::endl;
}

std::vector<uint8_t> createNormalCommand() {
    return {0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x03, 0x00, 0x00, 0x00, 0x01};
}

std::vector<uint8_t> createMaliciousCommand() {
    return {0x00, 0x02, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0x01, 0xC3, 0x50};
}

int main() {
    std::cout << "=== VoltGuard: Modbus Parser Demo ===\n";
    
    auto normal = createNormalCommand();
    auto parsedNormal = parseModbusTCP(normal);
    printPacket(parsedNormal);
    
    std::cout << "\nMalicious Packet:\n";
    auto malicious = createMaliciousCommand();
    auto parsedMal = parseModbusTCP(malicious);
    printPacket(parsedMal);
    
    return 0;
}
