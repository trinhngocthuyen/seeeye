module Pod
  class Hook
    def initialize(options)
      @installer = options[:installer]
    end

    def run
    end
  end
end
