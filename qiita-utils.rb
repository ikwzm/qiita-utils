#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
#
#       Version     :   0.0.1
#       Created     :   2024/8/1
#       File name   :   qiita-utils.rb
#       Author      :   Ichiro Kawazome <ichiro_k@ca2.so-net.ne.jp>
#       Description :   
#
#---------------------------------------------------------------------------------
#
#       Copyright (C) 2014-2024 Ichiro Kawazome
#       All rights reserved.
# 
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions
#       are met:
# 
#         1. Redistributions of source code must retain the above copyright
#            notice, this list of conditions and the following disclaimer.
# 
#         2. Redistributions in binary form must reproduce the above copyright
#            notice, this list of conditions and the following disclaimer in
#            the documentation and/or other materials provided with the
#            distribution.
# 
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
#---------------------------------------------------------------------------------
require 'pathname'
require 'optparse'
require 'yaml'
require 'json'

class QiitaUtility
  #-------------------------------------------------------------------------------
  # initialize    :
  #-------------------------------------------------------------------------------
  def initialize
    @program_name      = "qiita-utils"
    @program_version   = "0.0.1"
    @program_id        = @program_name + " " + @program_version
    @verbose           = false
    @dry_run           = false
    @debug             = false
    @item_post         = false
    @item_patch        = false
    @image_upload      = false
    @opt               = OptionParser.new do |opt|
      opt.program_name = @program_name
      opt.version      = @program_version
      opt.on("-v", "--verbose"              ){|val| @verbose          = true}
      opt.on("-d", "--debug"                ){|val| @debug            = true}
      opt.on("-n", "--dry-run"              ){|val| @dry_run          = true}
      opt.on("--item-post"                  ){|val| @item_post        = true}
      opt.on("--item-patch"                 ){|val| @item_patch       = true}
      opt.on("--image-upload"               ){|val| @image_upload     = true}
      opt.on("-i", "--input  YAML FILE NAME"){|val| @input_file_name  = val }
      opt.on("-o", "--output YAML FILE NAME"){|val| @output_file_name = val }
      opt.on("-f", "--config YAML FILE NAME"){|val| @input_file_name  = val
                                                    @output_file_name = val }
    end
  end

  #-------------------------------------------------------------------------------
  # parse_options :
  #-------------------------------------------------------------------------------
  def parse_options(argv)
    @opt.parse!(argv)
    if @input_file_name == nil then
      STDERR.puts "Error: Can Not YAML FILE NAME"
      STDERR.puts @opt.help
      exit(1)
    end
  end

  #-------------------------------------------------------------------------------
  # run_item_command :
  #-------------------------------------------------------------------------------
  def run_item_command(command, item_info)
    file_name = item_info["file_name"]
    if item_info.has_key?("stage") then
      if item_info["stage"] === "private" then
        command << " --private"
      end
      if item_info["stage"] === "public" then
        command << " --public"
      end
    end
    if item_info.has_key?("tags") then
      item_info["tags"].each do |tag|
        command << " --tags #{tag}"
      end
    end
    if item_info.has_key?("with_title") then
      if item_info["with_title"] == true then
        command << " --with_title"
      end
    end
    command << " #{file_name}"

    if @debug or @verbose or @dry_run then
      puts ("## #{command}")
    end
    if @dry_run == false then
      result_str  = `#{command}`
      result_info = JSON.load(result_str)
      ["title", "id", "url", "tags", "created_at", "updated_at"].each do |key|
        item_info[key] = result_info[key] if result_info.has_key?(key)
      end
      item_info["status"] = "Ok"
    end
  end
  
  #-------------------------------------------------------------------------------
  # item_post :
  #-------------------------------------------------------------------------------
  def item_post(item_info)
    if item_info.has_key?("id") then
      return
    end
    if item_info.has_key?("file_name") then
      file_name = item_info["file_name"]
    else
      return
    end
    if item_info.has_key?("stage") then
      if item_info["stage"] === "local" then
        return
      end
    end
    command = Pathname.new(__dir__).join("qiita-item.py").to_s
    command << " --post --json"
    run_item_command(command, item_info)
  end
  
  #-------------------------------------------------------------------------------
  # item_patch :
  #-------------------------------------------------------------------------------
  def item_patch(item_info)
    if item_info.has_key?("id") == nil then
      return
    else
      id = item_info["id"]
    end
    if item_info.has_key?("file_name") then
      file_name = item_info["file_name"]
    else
      return
    end
    if item_info.has_key?("stage") then
      if item_info["stage"] === "local" then
        return
      end
    end
    command = Pathname.new(__dir__).join("qiita-item.py").to_s
    command << " --patch #{id} --json"
    run_item_command(command, item_info)
  end
  
  #-------------------------------------------------------------------------------
  # image_upload :
  #-------------------------------------------------------------------------------
  def image_upload(image_info)
    if image_info.has_key?("url") then
      return
    end
    if image_info.has_key?("stage") then
      if image_info["stage"] == "local" then
        return
      end
    end
    if image_info.has_key?("file_name") then
      file_name = image_info["file_name"]
    else
      return
    end
    command = Pathname.new(__dir__).join("qiita-image-upload.py").to_s
    command << " --json"
    if image_info.has_key?("name") then
      name = image_info["name"]
      d_quarted = name.match(/^\"(.*)\"$/)
      s_quarted = name.match(/^\'(.*)\'$/)
      name = d_quarted[1] if d_quarted
      name = s_quarted[1] if s_quarted
      command << " --name \"#{name}\""
    end
    if image_info.has_key?("type") then
      type = image_info["type"]
      d_quarted = type.match(/^\"(.*)\"$/)
      s_quarted = type.match(/^\'(.*)\'$/)
      type = d_quarted[1] if d_quarted
      type = s_quarted[1] if s_quarted
      command << " --type \"#{type}\""
    end
    command << " #{file_name}"

    if @debug or @verbose or @dry_run then
      puts ("## #{command}")
    end
    if @dry_run == false then
      result_str  = `#{command}`
      result_info = JSON.load(result_str)
      ["name", "type", "url"].each do |key|
        image_info[key] = result_info[key] if result_info.has_key?(key)
      end
      image_info["status"] = "Ok"
    end
  end

  #-------------------------------------------------------------------------------
  # execute :
  #-------------------------------------------------------------------------------
  def execute
    input_info_list = Array.new
    File.open(@input_file_name) do |file|
      YAML.load_stream(file) do |input_info|
        input_info_list << input_info
      end
    end
    if @image_upload == true then
      input_info_list.each do |info|
        info.fetch("item_list", []).each do |item|
          if item.has_key?("image_list") then
            item["image_list"].each do |image_info|
              image_upload(image_info)
            end
          end
        end
        if info.has_key?("image_list") then
          info["image_list"].each do |image_info|
            image_upload(image_info)
          end
        end
      end
    end
    if @item_post == true then
      input_info_list.each do |info|
        info.fetch("item_list", []).each do |item|
          item_post(item)
        end
      end
    end
    if @item_patch == true then
      input_info_list.each do |info|
        info.fetch("item_list", []).each do |item|
          item_patch(item)
        end
      end
    end
    if @output_file_name != nil then
      File.open(@@output_file_name, "w") do |file|
        input_info_list.each do |info|
          YAML.dump(info, file)
        end
      end
    else
      input_info_list.each do |info|
        puts YAML.dump(info)
      end
    end
  end
end

if __FILE__ == $0
  util = QiitaUtility.new
  util.parse_options(ARGV)
  util.execute
end

