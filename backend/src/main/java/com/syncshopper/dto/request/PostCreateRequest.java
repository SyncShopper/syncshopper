package com.syncshopper.dto.request;

import com.syncshopper.domain.post.PostType;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class PostCreateRequest {

    @NotBlank(message = "Title is required")
    @Schema(description = "Post title", example = "System Maintenance Notice")
    private String title;

    @NotBlank(message = "Content is required")
    @Schema(description = "Post content", example = "System will be down for maintenance...")
    private String content;

    @NotNull(message = "Post type is required")
    @Schema(description = "Post type (NOTICE, FAQ, EVENT)", example = "NOTICE")
    private PostType postType;
}
