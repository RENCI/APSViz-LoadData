<?xml version="1.0" encoding="UTF-8"?><sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>maxinundepth_env_style</sld:Name>
    <sld:UserStyle>
      <sld:Name>maxinundepth_env_style</sld:Name>
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
              <sld:ColorMapEntry color="#0000CC" quantity="${env('q1',0.00)}" label="${env('l1','0.00 m')}"/>
              <sld:ColorMapEntry color="#0000FF" quantity="${env('q2',0.0625)}" label="${env('l2','0.06 m')}"/>
              <sld:ColorMapEntry color="#0033FF" quantity="${env('q3',0.125)}" label="${env('l3','0.13 m')}"/>
              <sld:ColorMapEntry color="#0066FF" quantity="${env('q4',0.1875)}" label="${env('l4','0.19 m')}"/>
              <sld:ColorMapEntry color="#0099FF" quantity="${env('q5',0.25)}" label="${env('l5','0.25 m')}"/>
              <sld:ColorMapEntry color="#00CCFF" quantity="${env('q6',0.3125)}" label="${env('l6','0.31 m')}"/>
              <sld:ColorMapEntry color="#00FFFF" quantity="${env('q7',0.375)}" label="${env('l7','0.38 m')}"/>
              <sld:ColorMapEntry color="#33FFCC" quantity="${env('q8',0.4375)}" label="${env('l8','0.44 m')}"/>
              <sld:ColorMapEntry color="#66FF99" quantity="${env('q9',0.50)}" label="${env('l9','0.50 m')}"/>
              <sld:ColorMapEntry color="#99FF66" quantity="${env('q10',0.5625)}" label="${env('l10','0.56 m')}"/>
              <sld:ColorMapEntry color="#CCFF33" quantity="${env('q11',0.625)}" label="${env('l11','0.63 m')}"/>
              <sld:ColorMapEntry color="#FFFF00" quantity="${env('q12',0.6875)}" label="${env('l12','0.69 m')}"/>
              <sld:ColorMapEntry color="#FFCC00" quantity="${env('q13',0.75)}" label="${env('l13','0.75 m')}"/>
              <sld:ColorMapEntry color="#FF9900" quantity="${env('q14',0.8125)}" label="${env('l14','0.81 m')}"/>
              <sld:ColorMapEntry color="#FF6600" quantity="${env('q15',0.875)}" label="${env('l15','0.88 m')}"/>
              <sld:ColorMapEntry color="#FF3300" quantity="${env('q16',0.9375)}" label="${env('l16','0.94 m')}"/>
              <sld:ColorMapEntry color="#FF0000" quantity="${env('q17',1.00)}" label="${env('l17','1.00 m')}"/>
            </sld:ColorMap>
            <sld:ContrastEnhancement/>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>