<?xml version="1.0" encoding="UTF-8"?><sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>swan_env_style</sld:Name>
    <sld:UserStyle>
      <sld:Name>swan_env_style</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Name>name</sld:Name>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
                <sld:ContrastEnhancement>
                  <sld:GammaValue>1.0</sld:GammaValue>
                </sld:ContrastEnhancement>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap>
              <sld:ColorMapEntry color="#30123B" quantity="${env('q1', 0.0)}" label="${env('l1', '0.0 m')}"/>
              <sld:ColorMapEntry color="#3D3790" quantity="${env('q2', 1.0)}" label="${env('l2', '1.0 m')}"/>
              <sld:ColorMapEntry color="#455ACD" quantity="${env('q3', 2.0)}" label="${env('l3', '2.0 m')}"/>
              <sld:ColorMapEntry color="#467BF3" quantity="${env('q4', 3.0)}" label="${env('l4', '3.0 m')}"/>
              <sld:ColorMapEntry color="#3E9BFF" quantity="${env('q5', 4.0)}" label="${env('l5', '4.0 m')}"/>
              <sld:ColorMapEntry color="#28BBEC" quantity="${env('q6', 5.0)}" label="${env('l6', '5.0 m')}"/>
              <sld:ColorMapEntry color="#18D7CC" quantity="${env('q7', 6.0)}" label="${env('l7', '6.0 m')}"/>
              <sld:ColorMapEntry color="#21EBAC" quantity="${env('q8', 7.0)}" label="${env('l8', '7.0 m')}"/>
              <sld:ColorMapEntry color="#46F884" quantity="${env('q9', 8.0)}" label="${env('l9', '8.0 m')}"/>
              <sld:ColorMapEntry color="#78FF5A" quantity="${env('q10', 9.0)}" label="${env('l10', '9.0 m')}"/>
              <sld:ColorMapEntry color="#A3FD3C" quantity="${env('q11', 10.0)}" label="${env('l11', '10.0 m')}"/>
              <sld:ColorMapEntry color="#C4F133" quantity="${env('q12', 11.0)}" label="${env('l12', '11.0 m')}"/>
              <sld:ColorMapEntry color="#E2DD37" quantity="${env('q13', 12.0)}" label="${env('l13', '12.0 m')}"/>
              <sld:ColorMapEntry color="#F6C33A" quantity="${env('q14', 13.0)}" label="${env('l14', '13.0 m')}"/>
              <sld:ColorMapEntry color="#FEA531" quantity="${env('q15', 14.0)}" label="${env('l15', '14.0 m')}"/>
              <sld:ColorMapEntry color="#FC8021" quantity="${env('q16', 15.0)}" label="${env('l16', '15.0 m')}"/>
              <sld:ColorMapEntry color="#F05B11" quantity="${env('q17', 16.0)}" label="${env('l17', '16.0 m')}"/>
              <sld:ColorMapEntry color="#DE3D08" quantity="${env('q18', 17.0)}" label="${env('l18', '17.0 m')}"/>
              <sld:ColorMapEntry color="#C42502" quantity="${env('q19', 18.0)}" label="${env('l19', '18.0 m')}"/>
              <sld:ColorMapEntry color="#A31201" quantity="${env('q20', 19.0)}" label="${env('l20', '19.0 m')}"/>
              <sld:ColorMapEntry color="#7A0402" quantity="${env('q21', 20.0)}" label="${env('l21', '20.0 m')}"/>
            </sld:ColorMap>
            <sld:ContrastEnhancement/>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>
