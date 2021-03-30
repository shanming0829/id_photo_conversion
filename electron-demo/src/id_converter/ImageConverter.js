/** ****************************************
*  Author : Shanming Liu
*  Created On : Mon Mar 29 2021
*  File : ImageConverter.js
*******************************************/
const sharp = require('sharp');
const {createCanvas} = require('canvas');

const WIDTH_1IN = 295;
const HEIGHT_1IN = 413;

const WIDTH_2IN = 413;
const HEIGHT_2IN = 626;

const WIDTH_5IN = 1500;
const HEIGHT_5IN = 1050;

// 非全景6寸照片
const WIDTH_6IN = 1950;
const HEIGHT_6IN = 1300;

const getCropRegion = (imageWidth, imageHeight, width, height) => {
  const rate = height / width;
  const imgRate = imageHeight / imageWidth;
  if (imgRate < rate) {
    // 左右裁剪
    x = (imageWidth - parseInt(imageHeight * width / height)) / 2;
    return {left: x, top: 0, width: imageWidth - x, height: imageHeight};
  } else {
    // 下裁剪, 保持头像一直存在
    y = parseInt(imageWidth * height / width);
    return {left: 0, top: 0, width: imageWidth, height: imageHeight - y};
  }
};

/**
 *
 * @param {Sharp} image The cropped image
 * @return {Sharp}
 */
const layoutImageSixToOne = async (image) =>{
  const canvas = createCanvas(200, 200);
  const ctx = canvas.getContext('2d');
  ctx.beginPath();
  ctx.moveTo(75, 50);
  ctx.lineTo(100, 75);
  ctx.lineTo(100, 25);
  ctx.fill();
  const buf = canvas.toBuffer('image/png');
  const img = sharp(buf);
  await img.toFile('test.png');
};

/**
 *
 * @param {string} source The source image file paths
 * @param {int|string} idInch The ID image size, e.g: 1 or 2
 * @param {int|string} photoInch The canvas image inch size, e.g: 5 or 6
 */
const convert = async (source, idInch, photoInch) =>{
  const sourceImage = sharp(source);
  const {width, height} = await sourceImage.metadata();
  const opt1 = getCropRegion(width, height, WIDTH_1IN, HEIGHT_1IN);
  const opt2 = getCropRegion(width, height, WIDTH_2IN, HEIGHT_2IN);

  const image1 = await sourceImage.clone().extract(opt1).resize(WIDTH_1IN, HEIGHT_1IN);
  // const image2 = await sourceImage.clone().extract(opt2).resize(WIDTH_2IN, HEIGHT_2IN);

  await layoutImageSixToOne(image1);
  // await image2.toFile('output2.png');
};

convert('C:\\Workspace\\cloud-env\\id_photo_conversion\\assets\\test.jpg', 1, 6);
// export default convert;
