require_relative "base"

module Pod
  class XCConfigsHook < Hook
    def run
      xcconfigs_dir = ".xcconfigs"
      target_support_files_root = @installer.sandbox.target_support_files_root
      target_support_files_root.glob("*/*.xcconfig").each do |path|
        target_name, config_name = path.basename.sub(/Pods-(.*)\.xcconfig/, '\1').to_s.split('.')
        include_paths = [
          "__base__.xcconfig",
          "#{target_name}.__base__.xcconfig",
          "#{target_name}.#{config_name}.xcconfig",
        ].map { |p| "#include? \"#{xcconfigs_dir}/#{p}\"" }
        content = File.open(path, &:read)
        File.open(path, "w") do |f|
          f.puts include_paths
          f.puts
          f.puts content
        end
      end
    end
  end
end
