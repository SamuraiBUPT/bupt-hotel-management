#include <crow_all.h>

int main(){
    crow::SimpleApp app;
    //测试
     CROW_ROUTE(app, "/test")([](){
        return "Hello world";
    });
    app.port(18888).multithreaded().run();
}