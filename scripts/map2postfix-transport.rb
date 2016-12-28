#!/bin/env ruby

map = ARGV[0] || File.expand_path(File.join(File.dirname(__FILE__),'..','sources','map.yml'))

unless File.exists?(map)
  STDERR.puts "No such map exists #{map}"
  STDERR.puts "USAGE: #{$0} map.yaml"
  exit 1
end

require 'yaml'

ymap = YAML.load_file(map)

longest_domain_length = ymap.values.collect{|e| Array(e) }.flatten.sort{|a,b| a.length <=> b.length }.last.length

puts ymap.keys.sort.collect{|os| Array(ymap[os]).sort.collect{|d| "%-#{longest_domain_length}s smtptor:[%s]" % [d,os] } }.flatten
