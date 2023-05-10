<?xml version="1.0" encoding="UTF-8"?><sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>maxwvel_env_style</sld:Name>
    <sld:UserStyle>
      <sld:Name>maxwvel_env_style</sld:Name>
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
              <sld:ColorMapEntry color="#3E26A9" quantity="${env('q1', 0.0)}" label="${env('l1', '0.0 m/s')}"/>
              <sld:ColorMapEntry color="#4433CD" quantity="${env('q2', 3.0)}" label="${env('l2', '3.0 m/s')}"/>
              <sld:ColorMapEntry color="#4743E8" quantity="${env('q3', 6.0)}" label="${env('l3', '6.0 m/s')}"/>
              <sld:ColorMapEntry color="#4755F6" quantity="${env('q4', 9.0)}" label="${env('l4', '9.0 m/s')}"/>
              <sld:ColorMapEntry color="#4367FE" quantity="${env('q5', 12.0)}" label="${env('l5', '12.0 m/s')}"/>
              <sld:ColorMapEntry color="#337AFD" quantity="${env('q6', 15.0)}" label="${env('l6', '15.0 m/s')}"/>
              <sld:ColorMapEntry color="#2D8CF4" quantity="${env('q7', 18.0)}" label="${env('l7', '18.0 m/s')}"/>
              <sld:ColorMapEntry color="#259CE8" quantity="${env('q8', 21.0)}" label="${env('l8', '21.0 m/s')}"/>
              <sld:ColorMapEntry color="#1BAADF" quantity="${env('q9', 24.0)}" label="${env('l9', '24.0 m/s')}"/>
              <sld:ColorMapEntry color="#04B6CE" quantity="${env('q10', 27.0)}" label="${env('l10', '27.0 m/s')}"/>
              <sld:ColorMapEntry color="#12BEB9" quantity="${env('q11', 30.0)}" label="${env('l11', '30.0 m/s')}"/>
              <sld:ColorMapEntry color="#2FC5A2" quantity="${env('q12', 33.0)}" label="${env('l12', '33.0 m/s')}"/>
              <sld:ColorMapEntry color="#47CB86" quantity="${env('q13', 36.0)}" label="${env('l13', '36.0 m/s')}"/>
              <sld:ColorMapEntry color="#71CD64" quantity="${env('q14', 39.0)}" label="${env('l14', '39.0 m/s')}"/>
              <sld:ColorMapEntry color="#9FC941" quantity="${env('q15', 42.0)}" label="${env('l15', '42.0 m/s')}"/>
              <sld:ColorMapEntry color="#C9C128" quantity="${env('q16', 45.0)}" label="${env('l16', '45.0 m/s')}"/>
              <sld:ColorMapEntry color="#EBBB30" quantity="${env('q17', 48.0)}" label="${env('l17', '48.0 m/s')}"/>
              <sld:ColorMapEntry color="#FFC13A" quantity="${env('q18', 51.0)}" label="${env('l18', '51.0 m/s')}"/>
              <sld:ColorMapEntry color="#FBD42E" quantity="${env('q19', 54.0)}" label="${env('l19', '54.0 m/s')}"/>
              <sld:ColorMapEntry color="#F5E824" quantity="${env('q20', 57.0)}" label="${env('l20', '57.0 m/s')}"/>
              <sld:ColorMapEntry color="#FAFB14" quantity="${env('q21', 60.0)}" label="${env('l21', '60.0 m/s')}"/>
            </sld:ColorMap>
            <sld:ContrastEnhancement/>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>
