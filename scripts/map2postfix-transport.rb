#!/bin/env ruby
#
# Generates a sorted list of domains and the onion services they map to.
# Sorting is done based on the onion service they map to, so that
# domains delivered to the same onion service are grouped together.
#

default_map = File.expand_path(File.join(File.dirname(__FILE__),'..','sources',
                                         'map.yml'))
maps = ARGV.empty? ? [ default_map ] : ARGV

maps.each do |map|
  unless File.exists?(map)
    STDERR.puts "No such map exists #{map}"
    STDERR.puts "USAGE: #{$0} map.yaml [ map2.yaml [ map3.yaml ] ]"
    exit 1
  end
end

require 'yaml'

merged_maps = maps.inject({}){|res,map| res.merge(YAML.load_file(map)) }

all_domains = merged_maps.values.collect{|e| Array(e) }.flatten
longest_domain_length = (all_domains.sort do |a,b|
  a.length <=> b.length
end).last.length

output = (merged_maps.keys.sort.collect do |os|
  Array(merged_maps[os]).sort.collect do |d|
    "%-#{longest_domain_length}s smtptor:[%s]" % [d,os]
  end
end).flatten

puts output
