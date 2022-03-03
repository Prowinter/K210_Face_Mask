#include "myiic.h"

//void SDA_IN(void)
//{
//	GPIO_InitTypeDef GPIO_InitStruct = {0};
//  GPIO_InitStruct.Pin = GPIO_PIN_13;
//  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
//  GPIO_InitStruct.Pull = GPIO_NOPULL;
//  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
//  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
//}

//void SDA_OUT(void)
//{
//	GPIO_InitTypeDef GPIO_InitStruct = {0};
//  GPIO_InitStruct.Pin = GPIO_PIN_13;
//  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
//  GPIO_InitStruct.Pull = GPIO_PULLUP;
//  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
//  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
//}

void delay_us(unsigned short int nus)
{
		__HAL_TIM_SetCounter(&DLY_TIM_Handle,0);
    HAL_TIM_Base_Start(&DLY_TIM_Handle);
    while(__HAL_TIM_GetCounter(&DLY_TIM_Handle)<nus);
    HAL_TIM_Base_Stop(&DLY_TIM_Handle);
}

//产生IIC起始信号
void IIC_Start(void)
{
	SDA_OUT(); 
	I2C_SDA_SET();	
	delay_us(5);
	I2C_SCLK_SET();
	delay_us(5);
 	I2C_SDA_RESET();
	delay_us(5);
	I2C_SCLK_RESET();
	delay_us(5);
}	  
//产生IIC停止信号
void IIC_Stop(void)
{
	SDA_OUT();//sda线输出
	delay_us(5);
	I2C_SCLK_RESET();
	delay_us(5);
	I2C_SDA_RESET();
	delay_us(5);
	I2C_SCLK_SET(); 
	delay_us(5);
	I2C_SDA_SET();		
	delay_us(4);
}

//等待应答信号到来
//返回值：1，接收应答失败
//        0，接收应答成功
unsigned char IIC_Wait_Ack(void)
{
	unsigned char ucErrTime=0;
	SDA_IN();      //SDA设置为输入  
	I2C_SDA_SET();   delay_us(1);
	I2C_SCLK_SET();delay_us(1);
	while(I2C_SDA_READ())
	{
		ucErrTime++;
		if(ucErrTime>250)
		{
			IIC_Stop();
			return 1;
		}
	}
	I2C_SCLK_RESET();
	return 0;  
} 
//产生ACK应答
void IIC_Ack(void)
{
	I2C_SCLK_RESET();
	SDA_OUT();
	I2C_SDA_RESET();
	delay_us(2);
	I2C_SCLK_SET();
	delay_us(2);
	I2C_SCLK_RESET();
}

//不产生ACK应答		    
void IIC_NAck(void)
{
	I2C_SCLK_RESET();
	SDA_OUT();
	I2C_SDA_SET();
	delay_us(2);
	I2C_SCLK_SET();
	delay_us(2);
	I2C_SCLK_RESET();
}	

//IIC发送一个字节
//返回从机有无应答
//1，有应答
//0，无应答			  
void IIC_Send_Byte(unsigned char txd)
{                        
	unsigned char t;   
	SDA_OUT(); 	    
	I2C_SCLK_RESET();
	for(t=0;t<8;t++)
	{              
		if((txd&0x80)>>7)
		{
			I2C_SDA_SET();
		}
		else
		{
			I2C_SDA_RESET();
		}
		txd<<=1; 
		delay_us(2);
		I2C_SCLK_SET();
		delay_us(6);
		I2C_SCLK_RESET();	
		delay_us(2);
	}	 
} 	    

//读1个字节，ack=1时，发送ACK，ack=0，发送nACK   
unsigned char IIC_Read_Byte(unsigned char ack)
{
	unsigned char i,receive=0;
	SDA_IN();//SDA设置为输入
	for(i=0;i<8;i++ )
	{
		I2C_SCLK_RESET(); 
		delay_us(2);
		I2C_SCLK_SET();
		receive<<=1;
		if(I2C_SDA_READ())receive++;
		delay_us(1);
	}					 
	if (!ack)
			IIC_NAck();
	else
			IIC_Ack(); 
	return receive;
}


float Get_Tem_DATA( unsigned char ReaAd)    //获取传感器所的温度值，℃，传入读取的RAM地址，输出摄氏度
{
	//从设备的地址 从0x00开始
	
	// temp=Get_Tem_DATA(0x07); 获取温度值
	
	
   //使用读的过程 ：写读命令  ，每次从高位到低位 

	unsigned char Pecreg = 0;
	unsigned char DataL = 0 ,DataH = 0;
	unsigned short int tem = 0;
	float Temp = 0;

	IIC_Start();

	IIC_Send_Byte(0x00); //  主机先发送写命令写入地址
	IIC_Wait_Ack();	
	IIC_Send_Byte(ReaAd); //  RAM地址0x07可以获得温度的信息   

	IIC_Wait_Ack();
	//------------
	IIC_Start();
	IIC_Send_Byte(0x01);  //主机发送读命令  	，从上面传送的地址中读取数据
	IIC_Wait_Ack();

	DataL=IIC_Read_Byte(1);
	DataH=IIC_Read_Byte(1);
	Pecreg=IIC_Read_Byte(1);
	IIC_Stop();
	tem = (DataH<<8) | DataL;;   //接收到传感器的16进制温度值
	//将16进制数值温度转换为℃  //不行，此处直接返回int型，会丢失小数数据，故还是返回浮点型
	Temp =  (((float)tem * 2) - 27315)/100;  //T= (DataH:DataL)*0.02-273.15  DataH:DataL=0x27AD,??? T=-70.01℃	  
	return Temp;
}


