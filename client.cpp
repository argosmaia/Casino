#include <iostream>
#include <boost/asio.hpp>
#include <thread>
#include "client.h"
#include "networkConfig.h"
#include "server.h"

using namespace boost::asio;
using namespace std;

void startClient(io_context& context, const string& host) {
    try {
        ip::tcp::resolver resolver(context);
        ip::tcp::resolver::results_type endpoints = resolver.resolve(host, to_string(PORT));  // Resolve o endereço do peer

        ip::tcp::socket socket(context);
        connect(socket, endpoints);  // Conecta ao peer

        // Envia uma mensagem
        string message = "Olá Cliente";
        write(socket, buffer(message));
        cout << "Mensagem enviada para o servidor!" << endl;

        // Recebe uma resposta do servidor
        char reply[1024];
        size_t len = socket.read_some(buffer(reply));
        cout << "Recebido do servidor: " << string(reply, len) << endl;
    } catch (exception& e) {
        cerr << "Erro no cliente: " << e.what() << endl;
    }
}
