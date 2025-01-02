#include <windows.h>
#include <stdio.h>
#include <string.h>

#define BTN_WIDTH 60
#define BTN_HEIGHT 40
#define CALC_WIDTH 280
#define CALC_HEIGHT 400

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void CreateCalculatorButtons(HWND);
void HandleButtonClick(HWND, int);

HWND displayField;
char displayBuffer[256] = "";
double firstNum = 0;
char operation = 0;
int newNumber = 1;

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    WNDCLASSEX wc = {0};
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.lpszClassName = "Calculator";
    RegisterClassEx(&wc);

    HWND hwnd = CreateWindowEx(
        0,
        "Calculator",
        "Calculator",
        WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT,
        CALC_WIDTH, CALC_HEIGHT,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg = {0};
    while(GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch(msg) {
        case WM_CREATE:
            displayField = CreateWindowEx(
                WS_EX_CLIENTEDGE,
                "EDIT",
                "",
                WS_CHILD | WS_VISIBLE | ES_RIGHT | ES_READONLY,
                20, 20, 
                CALC_WIDTH - 60, 30,
                hwnd,
                NULL,
                NULL,
                NULL
            );
            CreateCalculatorButtons(hwnd);
            break;

        case WM_COMMAND:
            if(HIWORD(wParam) == BN_CLICKED) {
                HandleButtonClick(hwnd, LOWORD(wParam));
            }
            break;

        case WM_DESTROY:
            PostQuitMessage(0);
            break;

        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

void CreateCalculatorButtons(HWND hwnd) {
    char* buttonLabels[] = {
        "7", "8", "9", "/",
        "4", "5", "6", "*",
        "1", "2", "3", "-",
        "0", ".", "=", "+",
        "C"
    };

    for(int i = 0; i < 4; i++) {
        for(int j = 0; j < 4; j++) {
            CreateWindow(
                "BUTTON",
                buttonLabels[i*4 + j],
                WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                20 + j*BTN_WIDTH, 70 + i*BTN_HEIGHT,
                BTN_WIDTH-10, BTN_HEIGHT-10,
                hwnd,
                (HMENU)(i*4 + j + 1),
                NULL,
                NULL
            );
        }
    }
    
    // Clear button
    CreateWindow(
        "BUTTON",
        buttonLabels[16],
        WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
        20, 70 + 4*BTN_HEIGHT,
        BTN_WIDTH-10, BTN_HEIGHT-10,
        hwnd,
        (HMENU)17,
        NULL,
        NULL
    );
}

void HandleButtonClick(HWND hwnd, int buttonId) {
    char buttonText[2];
    double result;
    double secondNum;

    if(buttonId >= 1 && buttonId <= 16) {
        char* buttonLabels[] = {
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        };
        strcpy(buttonText, buttonLabels[buttonId-1]);

        if(buttonText[0] >= '0' && buttonText[0] <= '9' || buttonText[0] == '.') {
            if(newNumber) {
                strcpy(displayBuffer, "");
                newNumber = 0;
            }
            strcat(displayBuffer, buttonText);
        }
        else if(buttonText[0] == '=') {
            secondNum = atof(displayBuffer);
            switch(operation) {
                case '+': result = firstNum + secondNum; break;
                case '-': result = firstNum - secondNum; break;
                case '*': result = firstNum * secondNum; break;
                case '/': result = firstNum / secondNum; break;
                default: result = secondNum;
            }
            sprintf(displayBuffer, "%.2f", result);
            operation = 0;
            newNumber = 1;
        }
        else {
            firstNum = atof(displayBuffer);
            operation = buttonText[0];
            newNumber = 1;
        }
    }
    else if(buttonId == 17) { // Clear
        strcpy(displayBuffer, "");
        firstNum = 0;
        operation = 0;
        newNumber = 1;
    }

    SetWindowText(displayField, displayBuffer);
}
