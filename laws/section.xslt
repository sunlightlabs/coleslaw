<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml"
                xmlns:html="http://www.w3.org/1999/xhtml" version="1.0"
                exclude-result-prefixes="html">
  <xsl:output method="html" indent="yes" encoding="UTF-8" />

  <xsl:template match="/uscfrag">
    <html>
      <head>
        <link rel="stylesheet" type="text/css" href="style.css" />
        <title>
          <xsl:value-of select="section/head" />
        </title>
      </head>
      <body>
        <div>
          <h3><xsl:value-of select="@titlenum" /> USC § <xsl:value-of select="section/head" /></h3>
          <xsl:apply-templates select="section/sectioncontent/psection" />
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="psection">
    <div>
      <xsl:attribute name="id">
        <xsl:value-of select="@id" />
      </xsl:attribute>
      <xsl:attribute name="class">psection level<xsl:value-of select="@lev" />
      </xsl:attribute>
      <span class="enum">
        <xsl:value-of select="string(enum)" />
      </span>
      <xsl:apply-templates select="text|head|psection" />
    </div>
  </xsl:template>

  <xsl:template match="text|head">
      <xsl:apply-templates select="text()|*" />
  </xsl:template>

  <xsl:template match="aref">
    <span>
      <xsl:attribute name="class">aref <xsl:value-of select="@type" /></xsl:attribute>          
      <xsl:apply-templates select="text()|*" />
    </span>
  </xsl:template>

  <xsl:template
      match="subref[@type='sec']|subref[@type='title']|subref[@type='psec']">
    <a>
      <xsl:attribute name="href">/laws/target/<xsl:value-of select="@target" /></xsl:attribute>
      <xsl:attribute name="class"><xsl:value-of select="@type" /></xsl:attribute>
      <xsl:value-of select="." />
    </a>
  </xsl:template>

  <xsl:template match="subref">
    <xsl:value-of select="." />
  </xsl:template>

  <xsl:template match="text()">
    <xsl:value-of select="." />
  </xsl:template>

</xsl:stylesheet>