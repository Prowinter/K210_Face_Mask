//////////////////////////////////////////////////////////////////////////////////	 
//I2C——HAL库初始化程序     By:Prowinter
//us级延时采用TIM定时提供 
//内含寄存器操作,具体修改请参考数据手册
//不会修改请注释相关内容转换为Hal库操作
////////////////////////////////////////////////////////////////////////////////// 	
#ifndef __MYIIC_H__
#define __MYIIC_H__
#include "stm32f1xx_hal.h"

#define SA                        0x00 
#define RAM_ACCESS                0x00 
#define EEPROM_ACCESS             0x20 
#define RAM_TOBJ1                 0x07 

#define DLY_TIM_Handle  htim2
extern TIM_HandleTypeDef DLY_TIM_Handle;
#define GPIOB_MODER_L            *(unsigned int*)(GPIOB_BASE+0x00)
#define GPIOB_MODER_H            *(unsigned int*)(GPIOB_BASE+0x04)
	
#define I2C_SCLK_GPIOx GPIOB
#define I2C_SCLK_GPIO_Pin GPIO_PIN_11

#define I2C_SDA_GPIOx GPIOB
#define I2C_SDA_Pin_Num 10
#define I2C_SDA_GPIO_Pin GPIO_PIN_10
#define Get_I2C_Pin_Num (I2C_SDA_Pin_Num>7?I2C_SDA_Pin_Num-8:I2C_SDA_Pin_Num)

/* 寄存器操作 */
#define SDA_IN()	{GPIOB_MODER_H&=0XFFFFF0FF;GPIOB_MODER_H|=8<<(4*Get_I2C_Pin_Num);}
#define SDA_OUT()	{GPIOB_MODER_H&=0XFFFFF0FF;GPIOB_MODER_H|=3<<(4*Get_I2C_Pin_Num);}


#define I2C_SCLK_SET() HAL_GPIO_WritePin(I2C_SCLK_GPIOx, I2C_SCLK_GPIO_Pin, GPIO_PIN_SET)
#define I2C_SCLK_RESET() HAL_GPIO_WritePin(I2C_SCLK_GPIOx, I2C_SCLK_GPIO_Pin, GPIO_PIN_RESET)

#define I2C_SDA_SET() HAL_GPIO_WritePin(I2C_SDA_GPIOx, I2C_SDA_GPIO_Pin, GPIO_PIN_SET)
#define I2C_SDA_RESET() HAL_GPIO_WritePin(I2C_SDA_GPIOx, I2C_SDA_GPIO_Pin, GPIO_PIN_RESET)
#define I2C_SDA_READ() HAL_GPIO_ReadPin(I2C_SDA_GPIOx, I2C_SDA_GPIO_Pin)

//IO方向设置
//IO操作函数	

//IIC所有操作函数
/* Hal库操作*/
//void SDA_IN(void);
//void SDA_OUT(void);

			 
void IIC_Start(void);															//发送IIC开始信号
void IIC_Stop(void);	  													//发送IIC停止信号
void IIC_Ack(void);																//IIC发送ACK信号
void IIC_NAck(void);															//IIC不发送ACK信号
void IIC_Send_Byte(unsigned char txd);						//IIC发送一个字节
unsigned char IIC_Read_Byte(unsigned char ack);		//IIC读取一个字节
unsigned char IIC_Wait_Ack(void); 								//IIC等待ACK信号
void delay_us(unsigned short int nus);
float Get_Tem_DATA( unsigned char ReaAd);
#endif
















