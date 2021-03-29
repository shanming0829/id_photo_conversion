/** ****************************************
*  Author : Shanming Liu
*  Created On : Mon Mar 29 2021
*  File : ImageConverter.js
*******************************************/
const sharp = require('sharp');

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

const layoutImageSixToOne = (image) =>{
  bk = sharp({
    create: {
      width: 300,
      height: 200,
      channels: 3,
      background: {r: 255, g: 255, b: 255},
    },
  });
  // // # 创建画笔
  // draw = ImageDraw.Draw(bk)
  // draw.line([(0, WIDTH_6IN * 0.25), (WIDTH_6IN, WIDTH_6IN * 0.25)],
  //           fill=128)
  // draw.line([(0, WIDTH_6IN * 0.5), (WIDTH_6IN, WIDTH_6IN * 0.5)],
  //           fill=128)
  // draw.line([(0, WIDTH_6IN * 0.75), (WIDTH_6IN, WIDTH_6IN * 0.75)],
  //           fill=128)
  // draw.line([(HEIGHT_6IN * 0.25, 0), (HEIGHT_6IN * 0.25, WIDTH_6IN)],
  //           fill=128)
  // draw.line([(HEIGHT_6IN * 0.5, 0), (HEIGHT_6IN * 0.5, WIDTH_6IN)],
  //           fill=128)
  // draw.line([(HEIGHT_6IN * 0.75, 0), (HEIGHT_6IN * 0.75, WIDTH_6IN)],
  //           fill=128)
  // focus_point = [0.125 * HEIGHT_6IN, 0.125 * WIDTH_6IN]
  // start_point = [
  //     focus_point[0] - 0.5 * WIDTH_1IN, focus_point[1] - 0.5 * HEIGHT_1IN
  // ]
  // for i in range(0, 4):
  //     for k in range(0, 4):
  //         bk.paste(photo, (int(start_point[0] + (k * HEIGHT_6IN / 4)),
  //                          int(start_point[1] + i * 0.25 * WIDTH_6IN)))
  // return bk
};


const convert = (source, idInch, photoInch) => {
  const sourceImage = sharp(source);
  return sourceImage.metadata().then((info) => {
    const opt1 = getCropRegion(info.width, info.height,
        WIDTH_1IN, HEIGHT_1IN);
    const opt2 = getCropRegion(info.width, info.height,
        WIDTH_2IN, HEIGHT_2IN);
    const image1 = sourceImage.extract(opt1).resize(WIDTH_1IN, HEIGHT_1IN);
    const image2 = sourceImage.extract(opt2).resize(WIDTH_2IN, HEIGHT_2IN);

    if (idInch == '1' || idInch == '2') {
      convertedImage = image1;
    } else {
      convertedImage = image2;
    }
    convertedImage.toFile('output.png', (err, info) => {
      console.log(info);
    });
  });
};

convert('C:\\Workspace\\cloud-env\\id_photo_conversion\\assets\\test.jpg', 1, 6)
// export default convert;
