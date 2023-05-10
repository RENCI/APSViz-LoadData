<?xml version="1.0" encoding="UTF-8"?><sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>maxele_env_style</sld:Name>
    <sld:UserStyle>
      <sld:Name>maxele_env_style</sld:Name>
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
	      <sld:ColorMapEntry color="#0000FF" quantity="${env('q2',0.25)}" label="${env('l2','0.25 m')}"/> 
	      <sld:ColorMapEntry color="#0033FF" quantity="${env('q3',0.50)}" label="${env('l3','0.50 m')}"/> 
	      <sld:ColorMapEntry color="#0066FF" quantity="${env('q4',0.75)}" label="${env('l4','0.75 m')}"/> 
	      <sld:ColorMapEntry color="#0099FF" quantity="${env('q5',1.00)}" label="${env('l5','1.00 m')}"/> 
	      <sld:ColorMapEntry color="#00CCFF" quantity="${env('q6',1.25)}" label="${env('l6','1.25 m')}"/> 
	      <sld:ColorMapEntry color="#00FFFF" quantity="${env('q7',1.50)}" label="${env('l7','1.50 m')}"/> 
	      <sld:ColorMapEntry color="#33FFCC" quantity="${env('q8',1.75)}" label="${env('l8','1.75 m')}"/> 
	      <sld:ColorMapEntry color="#66FF99" quantity="${env('q9',2.00)}" label="${env('l9','2.00 m')}"/> 
	      <sld:ColorMapEntry color="#99FF66" quantity="${env('q10',2.25)}" label="${env('l10','2.25 m')}"/> 
	      <sld:ColorMapEntry color="#CCFF33" quantity="${env('q11',2.50)}" label="${env('l11','2.50 m')}"/> 
	      <sld:ColorMapEntry color="#FFFF00" quantity="${env('q12',2.75)}" label="${env('l12','2.75 m')}"/> 
	      <sld:ColorMapEntry color="#FFCC00" quantity="${env('q13',3.00)}" label="${env('l13','3.00 m')}"/> 
	      <sld:ColorMapEntry color="#FF9900" quantity="${env('q14',3.25)}" label="${env('l14','3.25 m')}"/> 
	      <sld:ColorMapEntry color="#FF6600" quantity="${env('q15',3.50)}" label="${env('l15','3.50 m')}"/> 
	      <sld:ColorMapEntry color="#FF3300" quantity="${env('q16',3.75)}" label="${env('l16','3.75 m')}"/> 
	      <sld:ColorMapEntry color="#FF0000" quantity="${env('q17',4.00)}" label="${env('l17','4.00 m')}"/> 
            </sld:ColorMap>
            <sld:ContrastEnhancement/>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>
