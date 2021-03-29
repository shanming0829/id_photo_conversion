import React, {useState, useEffect} from 'react';
import PropTypes from 'prop-types';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import convert from './ImageConverter';

const IDInchList = ['1', '2', '1&2'];
const PhotoInchList = ['5', '6'];

const InchChoice = ({label, choices, onChange}) => {
  return (
    <Form.Group>
      <Form.Label>{label}</Form.Label>
      <Form.Control as="select" onChange={(evt) => onChange(evt.target.value)}>
        {choices.map((item) => <option key={item}>{item}</option>)}
      </Form.Control>
    </Form.Group>
  );
};

InchChoice.propTypes = {
  label: PropTypes.string.isRequired,
  choices: PropTypes.array.isRequired,
  onChange: PropTypes.func.isRequired,
};

const ConditionView = ({onConvertedImage}) => {
  const [selImage, setSelImage] = useState(null);
  const [idInch, setIdInch] = useState(IDInchList[0]);
  const [phoInch, setPhoInch] = useState(PhotoInchList[0]);

  const convertImage = () => {
    convertedImage = convert(selImage, idInch, phoInch);
    onConvertedImage(selImage);
  };

  useEffect(() => {
    convertImage();
  }, [selImage, idInch, phoInch]);

  return (
    <Row>
      <Col xs={6} md={3}>
        <InchChoice label="证件尺寸" choices={IDInchList} onChange={setIdInch}/>
      </Col>
      <Col xs={6} md={3}>
        <InchChoice label="照片尺寸" choices={PhotoInchList} onChange={setPhoInch}/>
      </Col>
      <Col xs={6} md={3}>
        <Form.Group>
          <Form.File id="idImportImage" label="导入图片"
            onChange={(evt) => setSelImage(evt.target.files[0].path)}/>
        </Form.Group>
      </Col>
      <Col xs={6} md={3}>
        <Form.Group>
          <Form.File id="idExportImage" label="导出图片" />
        </Form.Group>
      </Col>
    </Row>
  );
};

ConditionView.propTypes = {
  onConvertedImage: PropTypes.func.isRequired,
};

export default ConditionView;
