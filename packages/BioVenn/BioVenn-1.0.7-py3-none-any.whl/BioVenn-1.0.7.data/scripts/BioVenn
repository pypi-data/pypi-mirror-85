#!/usr/bin/env python

# Draw an area-proportional Venn diagram of 2 or 3 circles
#
# This function creates an area-proportional Venn diagram of 2 or 3 circles, based on lists of (biological) identifiers.
# It requires three parameters: input lists X, Y and Z. For a 2-circle Venn diagram, one of these lists
# should be left empty. Duplicate identifiers are removed automatically, and a mapping from Entrez and/or
# Affymetrix to Ensembl IDs is available. BioVenn is case-sensitive. In SVG mode, text and numbers can be dragged and dropped.
#
# When using a BioVenn diagram for a publication, please cite:
# BioVenn - a web application for the comparison and visualization of biological lists using area-proportional Venn diagrams
# T. Hulsen, J. de Vlieg and W. Alkema, BMC Genomics 2008, 9 (1): 488
#
# Parameters:
# list_x (Required) List with IDs from dataset X
# list_y (Required) List with IDs from dataset Y
# list_z (Required) List with IDs from dataset Z
# title (Optional) The title of the Venn diagram (default is "BioVenn")
# t_f (Optional) The font of the main title (default is "serif")
# t_fb (Optional) The font "face" of the main title (default is "bold")
# t_s (Optional) The size of the main title (default is 20)
# t_c (Optional) The colour of the main title (default is "black")
# subtitle (Optional) The subtitle of the Venn diagram (default is "(C) 2007-2020 Tim Hulsen")
# st_f (Optional) The font of the subtitle (default is "serif")
# st_fb (Optional) The font "face" of the subtitle (default is "bold")
# st_s (Optional) The size of the subtitle (default is 15)
# st_c (Optional) The colour of the subtitle (default is "black")
# xtitle (Optional) The X title of the Venn diagram (default is "ID set X")
# xt_f (Optional) The font of the X title (default is "serif")
# xt_fb (Optional) The font "face" of the X title (default is "bold")
# xt_s (Optional) The size of the X title (default is 10)
# xt_c (Optional) The colour of the X title (default is "black")
# ytitle (Optional) The Y title of the Venn diagram (default is "ID set Y")
# yt_f (Optional) The font of the Y title (default is "serif")
# yt_fb (Optional) The font "face" of the Y title (default is "bold")
# yt_s (Optional) The size of the Y title (default is 10)
# yt_c (Optional) The colour of the Y title (default is "black")
# ztitle (Optional) The Z title of the Venn diagram (default is "ID set Z")
# zt_f (Optional) The font of the Z title (default is "serif")
# zt_fb (Optional) The font "face" of the Z title (default is "bold")
# zt_s (Optional) The size of the Z title (default is 10)
# zt_c (Optional) The colour of the Z title (default is "black")
# nrtype (Optional) The type of the numbers to be displayed: absolute (abs) numbers or percentages (pct) (default is "abs")
# nr_f (Optional) The font of the numbers (default is "serif")
# nr_fb (Optional) The font "face" of the numbers (default is "bold")
# nr_s (Optional) The size of the numbers (default is 10)
# nr_c (Optional) The colour of the numbers (default is "black")
# x_c (Optional) The colour of the X circle (default is "red")
# y_c (Optional) The colour of the X circle (default is "green")
# z_c (Optional) The colour of the X circle (default is "blue")
# bg_c (Optional) The background colour (default is "white")
# width (Optional) The width of the output file (in pixels; default is 1000)
# height (Optional) The height of the output file (in pixels; default is 1000)
# output (Optional) Output format: "jpg","pdf","png","svg" or "tif" (anything else writes to the screen; default is "screen")
# filename (Optional) The name of the output file (default is "biovenn" + extension of the selected output format)
# map2ens (Optional) Map from Entrez or Affymetrix IDs to Ensembl IDs (default is False)
#
# Returns:
# An image of the Venn diagram is generated in the desired output format.
# Also returns an object with thirteen lists: X, Y, Z, X only, Y only, Z only, XY, XZ, YZ, XY only, XZ only, YZ only, XYZ.
#
# Example:
# list_x = ("1007_s_at","1053_at","117_at","121_at","1255_g_at","1294_at")
# list_y = ("1255_g_at","1294_at","1316_at","1320_at","1405_i_at")
# list_z = ("1007_s_at","1405_i_at","1255_g_at","1431_at","1438_at","1487_at","1494_f_at")
# biovenn = draw_venn(list_x, list_y, list_z, subtitle="Example diagram", nrtype="abs")

from biomart import BiomartServer
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy
import os
import re

def draw_venn(list_x, list_y, list_z, title="BioVenn", t_f="serif", t_fb="bold", t_s=20, t_c="black", subtitle="(C) 2007-2020 Tim Hulsen", st_f="serif", st_fb="bold", st_s=15, st_c="black", xtitle="ID Set X", xt_f="serif", xt_fb="bold", xt_s=10, xt_c="black", ytitle="ID Set Y", yt_f="serif", yt_fb="bold", yt_s=10, yt_c="black", ztitle="ID Set Z", zt_f="serif", zt_fb="bold", zt_s=10, zt_c="black", nrtype="abs", nr_f="serif", nr_fb="bold", nr_s=10, nr_c="black", x_c="red", y_c="green", z_c="blue", bg_c="white", width=1000, height=1000, output="screen", filename=None, map2ens=False):
  # Make input lists unique
  list_x = numpy.unique(list_x).tolist()
  list_y = numpy.unique(list_y).tolist()
  list_z = numpy.unique(list_z).tolist()

  # Convert to Ensembl IDs
  if map2ens:
    server = BiomartServer("http://www.ensembl.org/biomart")
    ensembl = server.datasets["hsapiens_gene_ensembl"]
    if len(list_x)>0:
      list_x_1 = ensembl.search({"filters":{"affy_hg_u133a":list_x},'attributes':['ensembl_gene_id']}).content.decode('UTF-8').split()
      list_x_2 = ensembl.search({"filters":{"entrezgene_id":list_x},'attributes':['ensembl_gene_id']}).content.decode('UTF-8').split()
      list_x = numpy.unique(list_x_1+list_x_2).tolist()
    if len(list_y)>0:
      list_y_1 = ensembl.search({"filters":{"affy_hg_u133a":list_y},'attributes':['ensembl_gene_id']}).content.decode('UTF-8').split()
      list_y_2 = ensembl.search({"filters":{"entrezgene_id":list_y},'attributes':['ensembl_gene_id']}).content.decode('UTF-8').split()
      list_y = numpy.unique(list_y_1+list_y_2).tolist()
    if len(list_z)>0:
      list_z_1 = ensembl.search({"filters":{"affy_hg_u133a":list_z},'attributes':['ensembl_gene_id']}).content.decode('UTF-8').split()
      list_z_2 = ensembl.search({"filters":{"entrezgene_id":list_z},'attributes':['ensembl_gene_id']}).content.decode('UTF-8').split()
      list_z = numpy.unique(list_z_1+list_z_2).tolist()

  # Generate lists and calculate numbers
  x = len(list_x)
  y = len(list_y)
  z = len(list_z)
  list_xy = list(set(list_x).intersection(set(list_y)))
  xy = len(list_xy)
  list_xz = list(set(list_x).intersection(set(list_z)))
  xz = len(list_xz)
  list_yz = list(set(list_y).intersection(set(list_z)))
  yz = len(list_yz)
  list_xyz = list(set(list_xy).intersection(set(list_z)))
  xyz = len(list_xyz)
  list_xy_only = list(set(list_xy).difference(set(list_xyz)))
  xy_only = len(list_xy_only)
  list_xz_only = list(set(list_xz).difference(set(list_xyz)))
  xz_only = len(list_xz_only)
  list_yz_only = list(set(list_yz).difference(set(list_xyz)))
  yz_only = len(list_yz_only)
  list_x_only = list(set(list_x).difference(set(list_xy+list_xz)))
  x_only = len(list_x_only)
  list_y_only = list(set(list_y).difference(set(list_xy+list_yz)))
  y_only = len(list_y_only)
  list_z_only = list(set(list_z).difference(set(list_xz+list_yz)))
  z_only = len(list_z_only)

  # Print numerical output
  print("x total:",x)
  print("y total:",y)
  print("z total:",z)
  print("x only:",x_only)
  print("y only:",y_only)
  print("z only:",z_only)
  print("x-y total overlap:",xy)
  print("x-z total overlap:",xz)
  print("y-z total overlap:",yz)
  print("x-y only overlap:",xy_only)
  print("x-z only overlap:",xz_only)
  print("y-z only overlap:",yz_only)
  print("x-y-z overlap:",xyz)

  # Define sq function
  def sq(nr):
    nr=nr**2
    return nr

  # Define sqr function
  def sqr(nr):
    nr=math.sqrt(round(abs(nr)))
    return nr 

  # Define arccos function
  def arccos(nr):
    nr=math.acos(min(max(-1,round(nr,5)),1))
    return nr

  # Set width and height of plotting area
  width_p=1000
  height_p=1000

  # Amplification
  amp=100000/(x+y+z-xy-xz-yz+xyz)
  x_text=x
  x=x*amp
  y_text=y
  y=y*amp
  z_text=z
  z=z*amp
  xy_text=xy
  xy=xy*amp
  xz_text=xz
  xz=xz*amp
  yz_text=yz
  yz=yz*amp
  xyz_text=xyz
  xyz=xyz*amp
  total=x+y+z-xy-xz-yz+xyz
  total_text=x_text+y_text+z_text-xy_text-xz_text-yz_text+xyz_text

  # Radius calculation
  x_r=sqr(x/math.pi)
  y_r=sqr(y/math.pi)
  z_r=sqr(z/math.pi)

  # Distance calculation
  xy_d=x_r+y_r
  if x and y:
    while xy>sq(x_r)*arccos((sq(xy_d)+sq(x_r)-sq(y_r))/(2*xy_d*x_r))+sq(y_r)*arccos((sq(xy_d)+sq(y_r)-sq(x_r))/(2*xy_d*y_r))-0.5*sqr(round((xy_d+x_r+y_r)*(xy_d+x_r-y_r)*(xy_d-x_r+y_r)*(-xy_d+x_r+y_r),5)):
      xy_d=xy_d-min(x_r,y_r)/1000.0
  xz_d=x_r+z_r
  if x and z:
    while xz>sq(x_r)*arccos((sq(xz_d)+sq(x_r)-sq(z_r))/(2*xz_d*x_r))+sq(z_r)*arccos((sq(xz_d)+sq(z_r)-sq(x_r))/(2*xz_d*z_r))-0.5*sqr(round((xz_d+x_r+z_r)*(xz_d+x_r-z_r)*(xz_d-x_r+z_r)*(-xz_d+x_r+z_r),5)):
      xz_d=xz_d-min(x_r,z_r)/1000.0
  yz_d=y_r+z_r
  if y and z:
    while yz>sq(y_r)*arccos((sq(yz_d)+sq(y_r)-sq(z_r))/(2*yz_d*y_r))+sq(z_r)*arccos((sq(yz_d)+sq(z_r)-sq(y_r))/(2*yz_d*z_r))-0.5*sqr(round((yz_d+y_r+z_r)*(yz_d+y_r-z_r)*(yz_d-y_r+z_r)*(-yz_d+y_r+z_r),5)):
      yz_d=yz_d-min(y_r,z_r)/1000.0
  if xy_d>xz_d+yz_d:
    xy_d=xz_d+yz_d
  if xz_d>xy_d+yz_d:
    xz_d=xy_d+yz_d
  if yz_d>xy_d+xz_d:
    yz_d=xy_d+xz_d

  # Angle calculation
  x_a=arccos((sq(xy_d)+sq(xz_d)-sq(yz_d))/(2*xy_d*xz_d))
  y_a=arccos((sq(xy_d)+sq(yz_d)-sq(xz_d))/(2*xy_d*yz_d))
  z_a=arccos((sq(xz_d)+sq(yz_d)-sq(xy_d))/(2*xz_d*yz_d))
  x_yz=xz_d*math.sin(z_a)
  y_yz=xy_d*math.cos(y_a)

  # PPU calculation
  width_h=max(y_r+y_yz,x_r,z_r-yz_d+y_yz)+max(x_r,y_r-y_yz,z_r+yz_d-y_yz)
  ppu_h=width_p/width_h
  width_v=max(x_r+x_yz,y_r,z_r)+max(y_r,z_r,x_r-x_yz)
  ppu_v=height_p/width_v
  ppu=min(ppu_h,ppu_v)

  # Circle center calculation
  x_h=max(x_r,y_r+y_yz,z_r-yz_d+y_yz)
  x_v=max(x_r,y_r-x_yz,z_r-x_yz)
  y_h=max(x_r-y_yz,y_r,z_r-yz_d)
  y_v=max(x_r+x_yz,y_r,z_r)
  z_h=max(x_r+yz_d-y_yz,y_r+yz_d,z_r)
  z_v=max(x_r+x_yz,y_r,z_r)

  # Calculate intersection points X-Y (first inner, then outer)
  xy_i_h_part1=(x_h+y_h)/2+((y_h-x_h)*(sq(x_r)-sq(y_r)))/(2*sq(xy_d))
  xy_i_v_part1=(x_v+y_v)/2+((y_v-x_v)*(sq(x_r)-sq(y_r)))/(2*sq(xy_d))
  xy_i_h_part2=2*((x_v-y_v)/sq(xy_d))*sqr((xy_d+x_r+y_r)*(xy_d+x_r-y_r)*(xy_d-x_r+y_r)*(-xy_d+x_r+y_r))/4
  xy_i_v_part2=2*((x_h-y_h)/sq(xy_d))*sqr((xy_d+x_r+y_r)*(xy_d+x_r-y_r)*(xy_d-x_r+y_r)*(-xy_d+x_r+y_r))/4
  xy_i1_h=xy_i_h_part1-xy_i_h_part2
  xy_i1_v=xy_i_v_part1+xy_i_v_part2
  xy_i2_h=xy_i_h_part1+xy_i_h_part2
  xy_i2_v=xy_i_v_part1-xy_i_v_part2

  # Calculate intersection points X-Z (first inner, then outer)
  xz_i_h_part1=(x_h+z_h)/2+((z_h-x_h)*(sq(x_r)-sq(z_r)))/(2*sq(xz_d))
  xz_i_v_part1=(x_v+z_v)/2+((z_v-x_v)*(sq(x_r)-sq(z_r)))/(2*sq(xz_d))
  xz_i_h_part2=2*((x_v-z_v)/sq(xz_d))*sqr((xz_d+x_r+z_r)*(xz_d+x_r-z_r)*(xz_d-x_r+z_r)*(-xz_d+x_r+z_r))/4
  xz_i_v_part2=2*((x_h-z_h)/sq(xz_d))*sqr((xz_d+x_r+z_r)*(xz_d+x_r-z_r)*(xz_d-x_r+z_r)*(-xz_d+x_r+z_r))/4
  xz_i1_h=xz_i_h_part1+xz_i_h_part2
  xz_i1_v=xz_i_v_part1-xz_i_v_part2
  xz_i2_h=xz_i_h_part1-xz_i_h_part2
  xz_i2_v=xz_i_v_part1+xz_i_v_part2

  # Calculate intersection points Y-Z (first inner, then outer)
  yz_i_h_part1=(y_h+z_h)/2+((z_h-y_h)*(sq(y_r)-sq(z_r)))/(2*sq(yz_d))
  yz_i_v_part1=(y_v+z_v)/2+((z_v-y_v)*(sq(y_r)-sq(z_r)))/(2*sq(yz_d))
  yz_i_h_part2=2*((y_v-z_v)/sq(yz_d))*sqr((yz_d+y_r+z_r)*(yz_d+y_r-z_r)*(yz_d-y_r+z_r)*(-yz_d+y_r+z_r))/4
  yz_i_v_part2=2*((y_h-z_h)/sq(yz_d))*sqr((yz_d+y_r+z_r)*(yz_d+y_r-z_r)*(yz_d-y_r+z_r)*(-yz_d+y_r+z_r))/4
  yz_i1_h=yz_i_h_part1-yz_i_h_part2
  yz_i1_v=yz_i_v_part1+yz_i_v_part2
  yz_i2_h=yz_i_h_part1+yz_i_h_part2
  yz_i2_v=yz_i_v_part1-yz_i_v_part2

  # Number fill point calculation of overlaps
  xy_f_h=(xy_i2_h+xz_i1_h+yz_i1_h)/3
  xy_f_v=(xy_i2_v+xz_i1_v+yz_i1_v)/3
  xz_f_h=(xy_i1_h+xz_i2_h+yz_i1_h)/3
  xz_f_v=(xy_i1_v+xz_i2_v+yz_i1_v)/3
  yz_f_h=(xy_i1_h+xz_i1_h+yz_i2_h)/3
  yz_f_v=(xy_i1_v+xz_i1_v+yz_i2_v)/3
  xyz_f_h=(xy_i1_h+xz_i1_h+yz_i1_h)/3
  xyz_f_v=(xy_i1_v+xz_i1_v+yz_i1_v)/3

  # Number fill point calculation of X
  # For XYZ diagrams
  if x and y and z:
    xyz_yz_i1=sqr(sq(xyz_f_h-yz_i1_h)+sq(xyz_f_v-yz_i1_v))
    x_ratio_h=(xyz_f_h-yz_i1_h)/xyz_yz_i1
    x_ratio_v=(xyz_f_v-yz_i1_v)/xyz_yz_i1
    x_out_h=x_h-x_r*x_ratio_h
    x_out_v=x_v-x_r*x_ratio_v
    x_f_h=(x_out_h+yz_i1_h)/2
    x_f_v=(x_out_v+yz_i1_v)/2
  # For XY diagrams
  elif x and y and not z:
    xy_f_h=(xy_i1_h+xy_i2_h)/2
    xy_f_v=(xy_i1_v+xy_i2_v)/2
    x_in_h=y_h+math.cos(y_a)*y_r
    x_in_v=y_v-math.sin(y_a)*y_r
    x_out_h=x_h+math.cos(y_a)*x_r
    x_out_v=x_v-math.sin(y_a)*x_r
    x_f_h=(x_out_h+x_in_h)/2
    x_f_v=(x_out_v+x_in_v)/2
  # For XZ diagrams
  elif x and not y and z:
    xz_f_h=(xz_i1_h+xz_i2_h)/2
    xz_f_v=(xz_i1_v+xz_i2_v)/2
    x_in_h=z_h-math.cos(z_a)*z_r
    x_in_v=z_v-math.sin(z_a)*z_r
    x_out_h=x_h-math.cos(z_a)*x_r
    x_out_v=x_v-math.sin(z_a)*x_r
    x_f_h=(x_out_h+x_in_h)/2
    x_f_v=(x_out_v+x_in_v)/2
  
  # Number fill point calculation of Y
  # For XYZ diagrams
  if x and y and z:
    xyz_xz_i1=sqr(sq(xyz_f_h-xz_i1_h)+sq(xyz_f_v-xz_i1_v))
    y_ratio_h=(xyz_f_h-xz_i1_h)/xyz_xz_i1
    y_ratio_v=(xyz_f_v-xz_i1_v)/xyz_xz_i1
    y_out_h=y_h-y_r*y_ratio_h
    y_out_v=y_v-y_r*y_ratio_v
    y_f_h=(y_out_h+xz_i1_h)/2
    y_f_v=(y_out_v+xz_i1_v)/2
  # For XY diagrams
  elif x and y and not z:
    xy_f_h=(xy_i1_h+xy_i2_h)/2
    xy_f_v=(xy_i1_v+xy_i2_v)/2
    y_in_h=x_h-math.cos(y_a)*x_r
    y_in_v=x_v+math.sin(y_a)*x_r
    y_out_h=y_h-math.cos(y_a)*y_r
    y_out_v=y_v+math.sin(y_a)*y_r
    y_f_h=(y_out_h+y_in_h)/2
    y_f_v=(y_out_v+y_in_v)/2
  # For YZ diagrams
  elif not x and y and z:
    yz_f_h=(yz_i1_h+yz_i2_h)/2
    yz_f_v=(yz_i1_v+yz_i2_v)/2
    y_in_h=z_h-z_r
    y_in_v=z_v
    y_out_h=y_h-y_r
    y_out_v=y_v
    y_f_h=(y_out_h+y_in_h)/2
    y_f_v=(y_out_v+y_in_v)/2

  # Number fill point calculation of Z
  # For XYZ diagrams
  if x and y and z:
    xyz_xy_i1=sqr(sq(xyz_f_h-xy_i1_h)+sq(xyz_f_v-xy_i1_v))
    z_ratio_h=(xyz_f_h-xy_i1_h)/xyz_xy_i1
    z_ratio_v=(xyz_f_v-xy_i1_v)/xyz_xy_i1
    z_out_h=z_h-z_r*z_ratio_h
    z_out_v=z_v-z_r*z_ratio_v
    z_f_h=(z_out_h+xy_i1_h)/2
    z_f_v=(z_out_v+xy_i1_v)/2
  # For XZ diagrams
  elif x and not y and z:
    xz_f_h=(xz_i1_h+xz_i2_h)/2
    xz_f_v=(xz_i1_v+xz_i2_v)/2
    z_in_h=x_h+math.cos(z_a)*x_r
    z_in_v=x_v+math.sin(z_a)*x_r
    z_out_h=z_h+math.cos(z_a)*z_r
    z_out_v=z_v+math.sin(z_a)*z_r
    z_f_h=(z_out_h+z_in_h)/2
    z_f_v=(z_out_v+z_in_v)/2
  # For YZ diagrams
  elif not x and y and z:
    yz_f_h=(yz_i1_h+yz_i2_h)/2
    yz_f_v=(yz_i1_v+yz_i2_v)/2
    z_in_h=y_h+z_r
    z_in_v=y_v
    z_out_h=z_h+y_r
    z_out_v=z_v
    z_f_h=(z_out_h+z_in_h)/2
    z_f_v=(z_out_v+z_in_v)/2

  # Number fill point calculation for special cases
  # No X only
  if x and not x_only:
    # X is subset of Z
    if not xy_only:
      xz_f_h=((y_h+y_r)+(x_h+x_r))/2
      xz_f_v=x_v
      yz_f_h=((z_h-z_r)+(x_h-x_r))/2
      yz_f_v=y_v
      xyz_f_h=((x_h-x_r)+(y_h+y_r))/2
      xyz_f_v=(x_v+y_v)/2
      y_f_h=((y_h-y_r)+(z_h-z_r))/2
      y_f_v=y_v
      xyz_xy_i2=sqr(sq(xyz_f_h-xy_i2_h)+sq(xyz_f_v-xy_i2_v))
      z_ratio_h=(xyz_f_h-xy_i2_h)/xyz_xy_i2
      z_ratio_v=(xyz_f_v-xy_i2_v)/xyz_xy_i2
      z_out_h=z_h-z_r*z_ratio_h
      z_out_v=z_v-z_r*z_ratio_v
      z_f_h=(z_out_h+xy_i2_h)/2
      z_f_v=(z_out_v+xy_i2_v)/2
    # X is subset of Y
    elif not xz_only:
      xy_f_h=((y_h-y_r)+(z_h-z_r))/2
      xy_f_v=x_v
      yz_f_h=((x_h+x_r)+(y_h+y_r))/2
      yz_f_v=z_v
      xyz_f_h=((z_h-z_r)+(x_h+x_r))/2
      xyz_f_v=(x_v+z_v)/2
      xyz_xz_i2=sqr(sq(xyz_f_h-xz_i2_h)+sq(xyz_f_v-xz_i2_v))
      y_ratio_h=(xyz_f_h-xz_i2_h)/xyz_xz_i2
      y_ratio_v=(xyz_f_v-xz_i2_v)/xyz_xz_i2
      y_out_h=y_h-y_r*y_ratio_h
      y_out_v=y_v-y_r*y_ratio_v
      y_f_h=(y_out_h+xz_i2_h)/2
      y_f_v=(y_out_v+xz_i2_v)/2
      z_f_h=((y_h+y_r)+(z_h+z_r))/2
      z_f_v=z_v
  # No Y only
  if y and not y_only:
    # Y is subset of Z
    if not xy_only:
      xz_f_h=((y_h+y_r)+(z_h+z_r))/2
      xz_f_v=x_v
      yz_f_h=((x_h-x_r)+(y_h-y_r))/2
      yz_f_v=y_v
      xyz_f_h=((x_h-x_r)+(y_h+y_r))/2
      xyz_f_v=(x_v+y_v)/2
      x_f_h=((z_h+z_r)+(x_h+x_r))/2
      x_f_v=x_v
      xyz_xy_i2=sqr(sq(xyz_f_h-xy_i2_h)+sq(xyz_f_v-xy_i2_v))
      z_ratio_h=(xyz_f_h-xy_i2_h)/xyz_xy_i2
      z_ratio_v=(xyz_f_v-xy_i2_v)/xyz_xy_i2
      z_out_h=z_h-z_r*z_ratio_h
      z_out_v=z_v-z_r*z_ratio_v
      z_f_h=(z_out_h+xy_i2_h)/2
      z_f_v=(z_out_v+xy_i2_v)/2
    # Y is subset of X
    elif not yz_only:
      xy_f_h=((y_h-y_r)+(z_h-z_r))/2
      xy_f_v=y_v
      xz_f_h=((y_h+y_r)+(x_h+x_r))/2
      xz_f_v=z_v
      xyz_f_h=((z_h-z_r)+(y_h+y_r))/2
      xyz_f_v=(y_v+z_v)/2
      xyz_yz_i1=sqr(sq(xyz_f_h-yz_i1_h)+sq(xyz_f_v-yz_i1_v))
      x_ratio_h=(xyz_f_h-yz_i1_h)/xyz_yz_i1
      x_ratio_v=(xyz_f_v-yz_i1_v)/xyz_yz_i1
      x_out_h=x_h-x_r*x_ratio_h
      x_out_v=x_v-x_r*x_ratio_v
      x_f_h=(x_out_h+yz_i1_h)/2
      x_f_v=(x_out_v+yz_i1_v)/2
      z_f_h=((x_h+x_r)+(z_h+z_r))/2
      z_f_v=y_v
  # No Z only
  if z and not z_only:
    # Z is subset of Y
    if not xz_only:
      xy_f_h=((y_h-y_r)+(z_h-z_r))/2
      xy_f_v=x_v
      yz_f_h=((x_h+x_r)+(z_h+z_r))/2
      yz_f_v=z_v
      xyz_f_h=((z_h-z_r)+(x_h+x_r))/2
      xyz_f_v=(x_v+z_v)/2
      xyz_xz_i2=sqr(sq(xyz_f_h-xz_i2_h)+sq(xyz_f_v-xz_i2_v))
      y_ratio_h=(xyz_f_h-xz_i2_h)/xyz_xz_i2
      y_ratio_v=(xyz_f_v-xz_i2_v)/xyz_xz_i2
      y_out_h=y_h-y_r*y_ratio_h
      y_out_v=y_v-y_r*y_ratio_v
      y_f_h=(y_out_h+xz_i2_h)/2
      y_f_v=(y_out_v+xz_i2_v)/2
      x_f_h=((x_h-x_r)+(y_h-y_r))/2
      x_f_v=x_v
    # Z is subset of X
    elif not yz_only:
      xy_f_h=((z_h-z_r)+(x_h-x_r))/2
      xy_f_v=y_v
      xz_f_h=((y_h+y_r)+(x_h+x_r))/2
      xz_f_v=x_v
      xyz_f_h=((z_h-z_r)+(y_h+y_r))/2
      xyz_f_v=(y_v+z_v)/2
      xyz_yz_i1=sqr(sq(xyz_f_h-yz_i1_h)+sq(xyz_f_v-yz_i1_v))
      x_ratio_h=(xyz_f_h-yz_i1_h)/xyz_yz_i1
      x_ratio_v=(xyz_f_v-yz_i1_v)/xyz_yz_i1
      x_out_h=x_h-x_r*x_ratio_h
      x_out_v=x_v-x_r*x_ratio_v
      x_f_h=(x_out_h+yz_i1_h)/2
      x_f_v=(x_out_v+yz_i1_v)/2
      y_f_h=((y_h-y_r)+(x_h-x_r))/2
      y_f_v=y_v

  # Draw circles
  fig,ax=plt.subplots(figsize=[width/100,height/100],dpi=100,facecolor=bg_c)
  ax.set(xlim=(0,width_p),ylim=(height_p,0),facecolor=bg_c)
  ax.set_aspect("equal",adjustable="box")
  ax.axis("off")
  plt.suptitle(title,fontproperties={"family":t_f,"size":t_s,"weight":t_fb},color=t_c,ha="center",va="center")
  plt.title(subtitle,fontdict={"fontfamily":st_f,"fontsize":st_s,"fontweight":st_fb,"color":st_c},pad=25)
  ax.add_artist(plt.Circle((ppu*x_h,ppu*x_v),ppu*x_r,color=x_c,alpha=0.5))
  ax.add_artist(plt.Circle((ppu*y_h,ppu*y_v),ppu*y_r,color=y_c,alpha=0.5))
  ax.add_artist(plt.Circle((ppu*z_h,ppu*z_v),ppu*z_r,color=z_c,alpha=0.5))

  # Print numbers
  if len(nrtype)>0:
    if nrtype=="abs":
      if x_only:
        plt.figtext(ppu*x_f_h,ppu*x_f_v,x_only,fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if y_only:
        plt.figtext(ppu*y_f_h,ppu*y_f_v,y_only,fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if z_only:
        plt.figtext(ppu*z_f_h,ppu*z_f_v,z_only,fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if xy_only:
        plt.figtext(ppu*xy_f_h,ppu*xy_f_v,xy_only,fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if xz_only:
        plt.figtext(ppu*xz_f_h,ppu*xz_f_v,xz_only,fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if yz_only:
        plt.figtext(ppu*yz_f_h,ppu*yz_f_v,yz_only,fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if xyz:
        plt.figtext(ppu*xyz_f_h,ppu*xyz_f_v,xyz_text,fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
    elif nrtype=="pct":
      if x_only:
        plt.figtext(ppu*x_f_h,ppu*x_f_v,str(round(x_only/total_text*100,2))+"%",fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if y_only:
        plt.figtext(ppu*y_f_h,ppu*y_f_v,str(round(y_only/total_text*100,2))+"%",fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if z_only:
        plt.figtext(ppu*z_f_h,ppu*z_f_v,str(round(z_only/total_text*100,2))+"%",fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if xy_only:
        plt.figtext(ppu*xy_f_h,ppu*xy_f_v,str(round(xy_only/total_text*100,2))+"%",fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if xz_only:
        plt.figtext(ppu*xz_f_h,ppu*xz_f_v,str(round(xz_only/total_text*100,2))+"%",fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if yz_only:
        plt.figtext(ppu*yz_f_h,ppu*yz_f_v,str(round(yz_only/total_text*100,2))+"%",fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)
      if xyz:
        plt.figtext(ppu*xyz_f_h,ppu*xyz_f_v,str(round(xyz_text/total_text*100,2))+"%",fontdict={"fontfamily":nr_f,"fontsize":nr_s,"fontweight":nr_fb,"color":nr_c},ha="center",va="center",transform=ax.transData)

  # Print texts
  if x:
    plt.figtext(ppu*x_h,ppu*x_v,xtitle,fontdict={"fontfamily":xt_f,"fontsize":xt_s,"fontweight":xt_fb,"color":xt_c},ha="center",va="center",transform=ax.transData)
  if y:
    plt.figtext(ppu*y_h,ppu*y_v,ytitle,fontdict={"fontfamily":yt_f,"fontsize":yt_s,"fontweight":yt_fb,"color":yt_c},ha="center",va="center",transform=ax.transData)
  if z:
    plt.figtext(ppu*z_h,ppu*z_v,ztitle,fontdict={"fontfamily":zt_f,"fontsize":zt_s,"fontweight":zt_fb,"color":zt_c},ha="center",va="center",transform=ax.transData)

  # Output to file or screen
  if output=="jpg":
    if not filename:
      filename="biovenn.jpg"
    plt.savefig(filename,format=output)
  elif output=="pdf":
    if not filename:
      filename="biovenn.pdf"
    plt.savefig(filename,format=output)
  elif output=="png":
    if not filename:
      filename="biovenn.png"
    plt.savefig(filename,format=output)
  elif output=="svg":
    if not filename:
      filename="biovenn.svg"
    plt.savefig("biovenn_temp.svg",format=output)
  elif output=="tif":
    if not filename:
      filename="biovenn.tif"
    plt.savefig(filename,format=output)
  else:
    plt.show()

  # Create drag-and-drop functionality for SVG file
  if output=="svg":
    svg_temp=open("biovenn_temp.svg","r")
    svg=open(filename,"w")
    id=1
    svglines=svg_temp.readlines()
    for svgline in svglines:
      if svgline[0:4]=="<svg":
        svgline=re.sub('viewBox="0 0 \\d* \\d*"','viewBox="0 0 '+str(width)+' '+str(height)+'"',svgline)
        svgline=re.sub('width="\\d*pt"','width="'+str(width)+'px"',svgline)
        svgline=re.sub('height="\\d*pt"','height="'+str(height)+'px"',svgline)
      if svgline[0:12]==" </metadata>":
        svgline=svgline.replace(" </metadata>",""" </metadata>
<script>
<![CDATA[
var Root=document.documentElement
standardize(Root)
function standardize(R){
  var Attr={
    'onmouseup':'add(evt)',
    'onmousedown':'grab(evt)',
    'onmousemove':null
  }
  assignAttr(R,Attr)
}
function grab(evt){
  var O=evt.target
  var Attr={
    'onmousemove':'slide(evt,\"'+O.id+'\")',
    'onmouseup':'standardize(Root)'
  }
  assignAttr(Root,Attr)
}
function slide(evt,id){
  if(id)
  {
    if(id.substr(0,2)=='g_'){
      var o=document.getElementById(id)
    }
    else if(document.getElementById(id).parentNode.id.substr(0,2)=='g_')
    {
      var o=document.getElementById(id).parentNode
    }
    else if(document.getElementById(id).parentNode.parentNode.id.substr(0,2)=='g_')
    {
      var o=document.getElementById(id).parentNode.parentNode
    }
    else if(document.getElementById(id).parentNode.parentNode.parentNode.id.substr(0,2)=='g_')
    {
      var o=document.getElementById(id).parentNode.parentNode.parentNode
    }
    if(o.transform.baseVal.getItem(0).type==SVGTransform.SVG_TRANSFORM_TRANSLATE)
    {
      var oldX=o.transform.baseVal.getItem(0).matrix.e,oldY=o.transform.baseVal.getItem(0).matrix.f;
      console.log(oldX+" "+oldY+" "+evt.clientX+" "+evt.clientY)
    }
    o.transform.baseVal.getItem(0).setTranslate(evt.clientX,evt.clientY);
  }
}
function assignAttr(O,A){
  for (i in A) O.setAttributeNS(null,i, A[i])
}
]]>
</script>""")
      elif svgline.find("<g transform")!=-1:
        svgline=svgline.replace("<g transform","<g id='g_"+str(id)+"' style='cursor:move' transform")
        id=id+1
      elif svgline.find("<use ")!=-1:
        svgline=svgline.replace("<use ","<use id='use_"+str(id)+"' ")
        id=id+1
      svg.write(svgline)
    svg_temp.close()
    os.remove("biovenn_temp.svg")
    svg.close()

  # Return lists
  return dict(x=list_x,y=list_y,z=list_z,x_only=list_x_only,y_only=list_y_only,z_only=list_z_only,xy=list_xy,xz=list_xz,yz=list_yz,xy_only=list_xy_only,xz_only=list_xz_only,yz_only=list_yz_only,xyz=list_xyz)
