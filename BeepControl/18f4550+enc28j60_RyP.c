#include <18F4550.h>
#device ADC=8
#use delay(clock=20000000)
#fuses HS,NOWDT,NOPROTECT,NOLVP,NODEBUG,USBDIV,VREGEN,NOPBADEN,WRTB

#byte porte = 0xF84
#byte trisc=0x87
#byte portc = 0x07
#byte trisa=0xff
#byte porta=0xff

/** Configuraci�n para el uso del stack tcip **/
#define STACK_USE_ICMP        1  //M�dulo de respuesta ICMP (ping)
#define STACK_USE_ARP         1  //Para solucionar direccionamiento MAC de las IP
#define STACK_USE_TCP         1  //Para enviar paquetes TCP 
#define STACK_USE_HTTP        1  //Uso de las funciones http del stack.
#define STACK_USE_CCS_PICENS  1  //CCS PICENS (Embedded Ethernet) 18F4620 + ENC28J60
#define STACK_USE_MCPENC      1  //Uso del enc28j60 por el stack (stacktsk.c)
#define STACK_USE_MAC         1  //Uso de la tarjeta de red
#define HTTP_SOCKET 80         //N� de puerto asociado al socket.
#define ENC_MAC_USE_SPI 1           //Uso del SPI por hardware
#define PIN_ENC_MAC_SO  PIN_B0      //Entrada serie de datos
#define PIN_ENC_MAC_CS  PIN_B2      //Chip select
#define PIN_ENC_MAC_RST PIN_B3      //Reset
#define PIN_ENC_MAC_INT PIN_B4      //Interrupci�n
#use STANDARD_IO( A )
#define PIN_LED_IN_1   PIN_A4
#define PIN_LED_IN_2   PIN_A5
#define PIN_LED_IN_3   PIN_A6
/******************************************************************************/

#define use_portd_lcd TRUE       //Uso del puerto d para control del lcd
#include <lcd.c>    //Carga librer�a del lcd de 4x20 para familia 18F
#include "tcpip/stacktsk.c"      //Carga el stack TCP/IP de Microchip 
/******************************************************************************/

/*********************  PAGINA WEB A MOSTRAR **********************************/
/* P�gina principal INDEX (/) */
const char  HTML_INDEX_PAGE[]="
<HTML><BODY BGCOLOR=#FFFFFF TEXT=#000000>

<center><H1>BeepControl </H1></center>
<BR><center><H2>Dashboard</H2></CENTER>


<FORM METHOD=GET>
<P>LCD: <INPUT TYPE=\"text\" NAME=\"lcd\" size=20 maxlength=16>
<input type=\"submit\" value=\"Enviar texto\">
</FORM>

<FORM METHOD=GET>
<input type=\"submit\" name=\"CM1\" value=\"A\">
<input type=\"submit\" name=\"CM1\" value=\"C\">
<input type=\"submit\" name=\"CM1\" value=\"Z\">
</FORM>
<FORM METHOD=GET>
<input type=\"submit\" name=\"CM2\" value=\"A\">
<input type=\"submit\" name=\"CM2\" value=\"C\">
<input type=\"submit\" name=\"CM2\" value=\"Z\">
</FORM>
<FORM METHOD=GET>
<input type=\"submit\" name=\"CM3\" value=\"A\">
<input type=\"submit\" name=\"CM3\" value=\"C\">
<input type=\"submit\" name=\"CM3\" value=\"Z\">
</FORM>
</BODY></HTML>
";

/* Elecci�n de MAC. No puede haber 2 dispositivos con misma MAC en una misma red
   Microchip Vendor ID  MAC: 00.04.A3.xx.xx.xx.  */
void MACAddrInit(void) {
   MY_MAC_BYTE1=0;
   MY_MAC_BYTE2=0x04;
   MY_MAC_BYTE3=0xA3;
   MY_MAC_BYTE4=0x06;
   MY_MAC_BYTE5=0x07;
   MY_MAC_BYTE6=0x08;
}

void IPAddrInit(void) {
   //Elecci�n de la direcci�n IP. 
   MY_IP_BYTE1=192;
   MY_IP_BYTE2=168;
   MY_IP_BYTE3=1;
   MY_IP_BYTE4=15;

   //Elecci�n de la direcci�n de puerta de enlace. 
   MY_GATE_BYTE1=192;
   MY_GATE_BYTE2=168;
   MY_GATE_BYTE3=1;
   MY_GATE_BYTE4=1;

   //Elecci�n de la m�scara de red.Si no se indica nada se tomar� 255.255.255.0
   MY_MASK_BYTE1=255;
   MY_MASK_BYTE2=255;
   MY_MASK_BYTE3=255;
   MY_MASK_BYTE4=0;
}

void moveServo(int16 puerto,int16 tiempo){
unsigned int i;
   for(i=0;i<60;i++){ 
      output_toggle(puerto);
      delay_us(tiempo);
      output_low(puerto);
    }}


void servoAccion(int servo, int accion)   //180 Degree
{
int16 puerto = PIN_C0;
int16 tiempoCerrar = 356;
int16 tiempoAbrir = 2150;

switch(servo){
   case 1:
      puerto = PIN_C0; break;
   case 2:
      puerto = PIN_C1; break;
   case 3:
      puerto = PIN_C2; break;
}

output_low(puerto); //Me aseguro que este apagado

switch(accion){
   case 0: //Cerrar
      moveServo(puerto,tiempoCerrar);
      break;
   case 1: //Abrir 180 grados
      moveServo(puerto,tiempoAbrir);
      break;
   case 2: //Abre y cierra
      moveServo(puerto,tiempoCerrar); //Me aseguro que se cierre
      moveServo(puerto,tiempoAbrir); //Lo abro
      delay_ms(1000); //Espero un segundo en maquina virtual, en no virtual es 3000 ms
      moveServo(puerto,tiempoCerrar); //Lo cierro
      break;
      }
}


/***************************  FUNCI�N GET PAGE   ******************************/
/* Esta funci�n devuelve la posici�n de memoria donde se encuentra la p�gina web 
a mostrar. En este caso se trata de una web con 2 p�ginas. Una principal index(/) 
y una secundaria(/lecturas)                                                   */

int32 http_get_page(char *file_str) {
   int32 file_loc=0;
   static char index[]="/";
 
   
   //printf(lcd_putc,"\fRequest %s ",file_str);      //Muestra en lcd solicitud

   /* Busca la posici�n de memoria donde se encuentra la p�gina solicitada */
   if (stricmp(file_str,index)==0)                 //Si es la principal...
      file_loc=label_address(HTML_INDEX_PAGE);     //...toma su posici�n en la memoria

   return(file_loc);
}

/**************************  FUNCI�N FORMAT CHAR  *****************************/
/* Con  la funci�n http_format_char  interconectamos las variables virtuales de 
la p�gina web con las variables del programa del PIC. Se encarga de enviar los 
cambios producidos en la aplicaci�n del PIC y reflejarlos en la aplicaci�n web. 
Muestra,por tanto, las lectura obtenidas por el PIC y las representa en la 
aplicaci�n de la p�gina web      

%0 es la variable virtual para representar el valor de la lectura del canal 
anal�gico
%1 es la variable virtual para representar el valor de la lectura del bit 0 del 
puerto E.
*/
int8 http_format_char(int32 file, char id, char *str, int8 max_ret) {
   char new_str[20];
   int8 len=0;
   int8 AD0;
   int8 RE0;

   *str=0;

   switch(id) {
      case '0':
         set_adc_channel(0);
         delay_us(100);
         AD0=read_adc();
         sprintf(new_str,"0x%X",AD0);
         len=strlen(new_str);
      break;
      case '1':
         RE0=bit_test(porte,0);
         sprintf(new_str,"%d",RE0);
         len=strlen(new_str);
      break;  
      default:
      len=0;
   }

   if (len)strncpy(str, new_str, max_ret);
   else  *str=0;
   
   return(len);
}

/***************************  FUNCI�N EXEC CGI   ******************************/
/* Con la funci�n http_exec_cgi interconectamos las variables virtuales de la 
p�gina web con las variables del programa del PIC. Se encarga de recibir 
los cambios producidos en la aplicaci�n web y reflejarlos en el hardware del PIC. 
Ejecuta, por tanto, la acci�n elegida seg�n el valor de la variable virtual recibida 
de la p�gina web

key es la variable virtual que viene de la pagina web
val es el valor de una variable virtual de la p�gina web
file es la direcci�n de la p�gina web devuelta por http__page ()

*/

void http_exec_cgi(int32 file, char *key, char *val) {
   static char boton1_key[]="CM1";
   static char boton2_key[]="CM2";
   static char boton3_key[]="CM3";
   static char lcd_key[]="lcd";
   int accionServo = 0;
   
   //Para ver en la pantalla los valores recibidos
  /*
   printf(lcd_putc,"\nKEY=%S", key);
   printf(lcd_putc,"\nVAL=%S", val);
  */
   
   switch (val){
   case "C": accionServo = 0; break;
   case "A": accionServo = 1; break;
   case "Z": accionServo = 2; break;
   }


   /* Se ejecutar� al recibir un request a CM1 */
   if (stricmp(key,boton1_key)==0) {
      servoAccion(1,accionServo);
   }
   /* Se ejecutar� al recibir un request a CM2 */
   if (stricmp(key,boton2_key)==0) {
      servoAccion(2,accionServo);
   }
   /* Se ejecutar� al recibir un request a CM3 */
   if (stricmp(key,boton3_key)==0) {
      servoAccion(3,accionServo);
   }
   /* Se ejecutar� al recibir un request a lcd */
   if (stricmp(key,lcd_key)==0) {
      printf(lcd_putc,"\f%s",val);  //Muestra en el lcd el texto recibido
   }
}


/************************** FUNCI�N PRINCIPAL *********************************/
void main(void) {
   /* Habilitaci�n y configuraci�n del canal anal�gico 0 */
   setup_adc(ADC_CLOCK_INTERNAL);
   setup_adc_ports(AN0);
   set_adc_channel(0);
   delay_ms(1);
   TRISA = 0xFF;
   int lab_no = 0;

   /*Reset de las salidas */
   output_low(PIN_C0);
   output_low(PIN_C1);
   output_low(PIN_C2);
    
   /* Inicializaci�n del lcd */
   lcd_init();
   printf(lcd_putc,"\fUniversidad APEC");   //Mensaje de inicio en lcd
   lcd_gotoxy(1,4);
   printf(lcd_putc,"Laboratorio: %u",lab_no);
   delay_ms(1000);
  
   /* Inicializaci�n del Stack */
   MACAddrInit(); //Se asigna la direcci�n MAC elegida 
   IPAddrInit();  //Se asigna IP, mascara de red y puerta de enlace elegidos
   StackInit();   //Inicializa el stack
   
   /* Muestra la IP elegida en lcd */
  /* printf(lcd_putc,"\nIP: %u.%u.%u.%u:%u", MY_IP_BYTE1, MY_IP_BYTE2, MY_IP_BYTE3, MY_IP_BYTE4,HTTP_SOCKET);
   delay_ms(10);*/
   while(TRUE) {
   StackTask();
   int pulsado = PORTA;

   if (pulsado == 4){
   pulsado = 0;
   lab_no = 1;
   lcd_gotoxy(1,3);
   printf(lcd_putc,"Laboratorio: %u",lab_no);
   servoAccion(1,2);
   }
   if (pulsado == 8){
   pulsado = 0;
   lab_no = 2;
   lcd_gotoxy(1,3);
   printf(lcd_putc,"Laboratorio: %u",lab_no);
   servoAccion(2,2);
   }
   if (pulsado == 16){
   pulsado = 0;
   lab_no = 3;
   lcd_gotoxy(1,3);
   printf(lcd_putc,"Laboratorio: %u",lab_no);
   servoAccion(3,2);
   }
}
   }
